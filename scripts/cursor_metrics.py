#!/usr/bin/env python3
"""
Cursor Metrics to Elasticsearch Script

This script fetches daily usage data from Cursor API and stores it in Elasticsearch
with enriched developer information.
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import hashlib
import time

import requests
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from requests.auth import HTTPBasicAuth

# Import the Cursor Score Calculator
from cursor_score_calculator import CursorScoreCalculator


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CursorMetricsCollector:
    """Collects Cursor metrics and stores them in Elasticsearch."""
    
    def __init__(self, cursor_api_url: str, cursor_auth: Tuple[str, str],
                 es_url: str, es_auth: Tuple[str, str], users_file: str = "users.txt"):
        """
        Initialize the collector.
        
        Args:
            cursor_api_url: Base URL for Cursor API
            cursor_auth: Tuple of (username, password) for Cursor API
            es_url: Elasticsearch URL
            es_auth: Tuple of (username, password) for Elasticsearch
            users_file: Path to users file with corporate names
        """
        self.cursor_api_url = cursor_api_url.rstrip('/')
        self.cursor_auth = HTTPBasicAuth(*cursor_auth)
        self.es_url = es_url
        self.es_auth = es_auth
        self.users_file = users_file
        
        # Initialize Elasticsearch client
        self.es = Elasticsearch(
            [es_url],
            http_auth=es_auth,
            verify_certs=False,
            timeout=30,
            max_retries=3,
            retry_on_timeout=True
        )
        
        # Initialize Cursor Score Calculator
        self.score_calculator = CursorScoreCalculator(minimum_activity_threshold=5)
        
        # Test connections
        self._test_connections()
        
        # Load corporate names mapping
        self.corporate_names = self._load_corporate_names()
        
    def _test_connections(self) -> None:
        """Test connections to Cursor API and Elasticsearch."""
        logger.info("Testing connections...")
        
        # Test Cursor API
        try:
            response = requests.get(
                f"{self.cursor_api_url}/teams/members",
                auth=self.cursor_auth,
                timeout=10
            )
            response.raise_for_status()
            logger.info("✓ Cursor API connection successful")
        except Exception as e:
            logger.error(f"✗ Cursor API connection failed: {e}")
            sys.exit(1)
        
        # Test Elasticsearch
        try:
            if self.es.ping():
                logger.info("✓ Elasticsearch connection successful")
            else:
                raise Exception("Ping failed")
        except Exception as e:
            logger.error(f"✗ Elasticsearch connection failed: {e}")
            sys.exit(1)
    
    def _load_corporate_names(self) -> Dict[str, str]:
        """Load corporate names from users file."""
        corporate_names = {}
        
        if not os.path.exists(self.users_file):
            logger.warning(f"Users file not found: {self.users_file}")
            return corporate_names
        
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split('-')
                    if len(parts) >= 2:
                        corporate_name = parts[0].strip()
                        identifier = parts[1].strip()
                        
                        # Check if identifier is an email
                        if '@' in identifier:
                            corporate_names[identifier] = corporate_name
                        else:
                            # It's a user ID, skip for now as we need email mapping
                            pass
                    else:
                        logger.warning(f"Invalid format in users file line {line_num}: {line}")
            
            logger.info(f"Loaded {len(corporate_names)} corporate name mappings")
            return corporate_names
            
        except Exception as e:
            logger.error(f"Error loading corporate names: {e}")
            return {}
    
    def fetch_team_members(self) -> Dict[str, Dict[str, str]]:
        """Fetch team members information from Cursor API."""
        logger.info("Fetching team members...")
        
        try:
            response = requests.get(
                f"{self.cursor_api_url}/teams/members",
                auth=self.cursor_auth,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            members = {}
            
            for member in data.get('teamMembers', []):
                email = member.get('email', '')
                if email:
                    members[email] = {
                        'name': member.get('name', ''),
                        'role': member.get('role', '')
                    }
            
            logger.info(f"Fetched {len(members)} team members")
            return members
            
        except Exception as e:
            logger.error(f"Error fetching team members: {e}")
            return {}
    
    def fetch_daily_usage_data(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Fetch daily usage data from Cursor API."""
        logger.info(f"Fetching daily usage data from {start_date} to {end_date}")
        
        # Convert dates to Unix timestamps in milliseconds
        start_timestamp = int(start_date.timestamp() * 1000)
        end_timestamp = int(end_date.timestamp() * 1000)
        
        payload = {
            "startDate": start_timestamp,
            "endDate": end_timestamp
        }
        
        try:
            response = requests.post(
                f"{self.cursor_api_url}/teams/daily-usage-data",
                auth=self.cursor_auth,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            data = response.json()
            usage_data = data.get('data', [])
            
            logger.info(f"Fetched {len(usage_data)} daily usage records")
            return usage_data
            
        except Exception as e:
            logger.error(f"Error fetching daily usage data: {e}")
            return []
    
    def fetch_filtered_usage_events(self, start_date: datetime = None, end_date: datetime = None) -> List[Dict]:
        """Fetch all filtered usage events from Cursor API with pagination."""
        logger.info("Fetching filtered usage events...")
        
        all_events = []
        current_page = 1
        total_pages = None
        
        # Prepare payload
        payload = {}
        if start_date and end_date:
            start_timestamp = int(start_date.timestamp() * 1000)
            end_timestamp = int(end_date.timestamp() * 1000)
            payload.update({
                "startDate": start_timestamp,
                "endDate": end_timestamp
            })
        
        while True:
            # Add page number to payload
            page_payload = payload.copy()
            if current_page > 1:
                page_payload["page"] = current_page
            
            try:
                logger.info(f"Fetching page {current_page}{f'/{total_pages}' if total_pages else ''}...")
                
                response = requests.post(
                    f"{self.cursor_api_url}/teams/filtered-usage-events",
                    auth=self.cursor_auth,
                    json=page_payload,
                    timeout=60
                )
                response.raise_for_status()
                
                data = response.json()
                
                # Extract pagination info
                pagination = data.get('pagination', {})
                total_pages = pagination.get('numPages', 1)
                has_next_page = pagination.get('hasNextPage', False)
                page_size = pagination.get('pageSize', 100)
                
                # Extract events
                events = data.get('usageEvents', [])
                all_events.extend(events)
                
                logger.info(f"Page {current_page}: fetched {len(events)} events "
                           f"(total so far: {len(all_events)})")
                
                # Check if we have more pages
                if not has_next_page:
                    break
                
                current_page += 1
                
                # Add small delay to avoid rate limiting
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error fetching filtered usage events page {current_page}: {e}")
                break
        
        logger.info(f"Fetched total of {len(all_events)} filtered usage events across {current_page} pages")
        return all_events
    
    def _generate_document_id(self, date: int, email: str, event_type: str = "daily") -> str:
        """Generate unique document ID from date, email and event type."""
        # Convert timestamp to date string for consistent ID
        if isinstance(date, str):
            # Handle string timestamps
            date_obj = datetime.fromtimestamp(int(date) / 1000)
        else:
            date_obj = datetime.fromtimestamp(date / 1000)
        
        date_str = date_obj.strftime('%Y-%m-%d')
        
        # For usage events, include timestamp for uniqueness
        if event_type == "usage_event":
            timestamp_str = str(date) if isinstance(date, str) else str(date)
            id_string = f"{event_type}-{timestamp_str}-{email}"
        else:
            id_string = f"{event_type}-{date_str}-{email}"
        
        return hashlib.sha256(id_string.encode()).hexdigest()[:16]
    
    def enrich_usage_data(self, usage_data: List[Dict], members: Dict[str, Dict[str, str]]) -> List[Dict]:
        """Enrich usage data with member names, corporate names, and Cursor Scores."""
        enriched_data = []
        
        for record in usage_data:
            email = record.get('email', '')
            
            # Create enriched record
            enriched_record = record.copy()
            
            # Add member information
            if email in members:
                enriched_record['memberName'] = members[email]['name']
                enriched_record['memberRole'] = members[email]['role']
            else:
                enriched_record['memberName'] = ''
                enriched_record['memberRole'] = ''
            
            # Add corporate name
            enriched_record['author'] = self.corporate_names.get(email, 'non')
            
            # Convert timestamp to readable date
            if 'date' in enriched_record:
                enriched_record['dateString'] = datetime.fromtimestamp(enriched_record['date'] / 1000).isoformat()
                enriched_record['date_string'] = datetime.fromtimestamp(enriched_record['date'] / 1000).isoformat()
            # Generate document ID
            enriched_record['_id'] = self._generate_document_id(
                enriched_record.get('date', 0), email, "daily"
            )
            
            # Add metadata
            enriched_record['@timestamp'] = datetime.utcnow().isoformat()
            enriched_record['ingestionDate'] = datetime.utcnow().strftime('%Y-%m-%d')
            
            enriched_data.append(enriched_record)
        
        # Calculate Cursor Scores for the entire dataset
        logger.info("Calculating Cursor Scores for daily usage data...")
        try:
            enriched_data_with_scores = self.score_calculator.calculate_scores_for_dataset(enriched_data)
            logger.info("✓ Cursor Score calculation completed successfully")
            return enriched_data_with_scores
        except Exception as e:
            logger.error(f"Error calculating Cursor Scores: {e}")
            # Return data without scores if calculation fails
            for record in enriched_data:
                record['cursorScore'] = 0
                record['cursorScoreStatus'] = 'calculation_failed'
                record['cursorScoreComponents'] = {}
            return enriched_data
    
    def enrich_usage_events(self, usage_events: List[Dict], members: Dict[str, Dict[str, str]]) -> List[Dict]:
        """Enrich usage events with member names and corporate names."""
        enriched_events = []
        
        for event in usage_events:
            email = event.get('userEmail', '')
            
            # Create enriched event
            enriched_event = event.copy()
            
            # Add member information
            if email in members:
                enriched_event['memberName'] = members[email]['name']
                enriched_event['memberRole'] = members[email]['role']
            else:
                enriched_event['memberName'] = ''
                enriched_event['memberRole'] = ''
            
            # Add corporate name
            enriched_event['author'] = self.corporate_names.get(email, '')
            
            # Convert timestamp to readable date and eventTimestamp
            if 'timestamp' in enriched_event:
                timestamp = int(enriched_event['timestamp'])
                timestamp_dt = datetime.fromtimestamp(timestamp / 1000)
                
                enriched_event['dateString'] = timestamp_dt.strftime('%Y-%m-%d')
                enriched_event['date_string'] = timestamp_dt.strftime('%Y-%m-%d')
                enriched_event['dateTimeString'] = timestamp_dt.strftime('%Y-%m-%d %H:%M:%S')
                
                # Add eventTimestamp field for Kibana data view
                enriched_event['eventTimestamp'] = timestamp_dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
            
            # Generate document ID using timestamp for uniqueness
            enriched_event['_id'] = self._generate_document_id(
                enriched_event.get('timestamp', '0'), email, "usage_event"
            )
            
            # Add metadata
            enriched_event['@timestamp'] = datetime.utcnow().isoformat()
            enriched_event['ingestionDate'] = datetime.utcnow().strftime('%Y-%m-%d')
            
            enriched_events.append(enriched_event)
        
        return enriched_events
    
    def create_elasticsearch_index(self, index_name: str) -> None:
        """Create Elasticsearch index with proper mapping."""
        mapping = {
            "mappings": {
                "properties": {
                    "date": {"type": "date", "format": "epoch_millis"},
                    "dateString": {"type": "date", "format": "yyyy-MM-dd"},
                    "date_string": {"type": "date", "format": "yyyy-MM-dd"},
                    "email": {"type": "keyword"},
                    "memberName": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                    "memberRole": {"type": "keyword"},
                    "author": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                    "isActive": {"type": "boolean"},
                    "totalLinesAdded": {"type": "long"},
                    "totalLinesDeleted": {"type": "long"},
                    "acceptedLinesAdded": {"type": "long"},
                    "acceptedLinesDeleted": {"type": "long"},
                    "totalApplies": {"type": "long"},
                    "totalAccepts": {"type": "long"},
                    "totalRejects": {"type": "long"},
                    "totalTabsShown": {"type": "long"},
                    "totalTabsAccepted": {"type": "long"},
                    "composerRequests": {"type": "long"},
                    "chatRequests": {"type": "long"},
                    "agentRequests": {"type": "long"},
                    "cmdkUsages": {"type": "long"},
                    "subscriptionIncludedReqs": {"type": "long"},
                    "apiKeyReqs": {"type": "long"},
                    "usageBasedReqs": {"type": "long"},
                    "bugbotUsages": {"type": "long"},
                    "mostUsedModel": {"type": "keyword"},
                    "applyMostUsedExtension": {"type": "keyword"},
                    "tabMostUsedExtension": {"type": "keyword"},
                    "clientVersion": {"type": "keyword"},
                    "@timestamp": {"type": "date"},
                    "ingestionDate": {"type": "date", "format": "yyyy-MM-dd"},
                    # Cursor Score fields
                    "cursorScore": {"type": "float"},
                    "cursorScoreStatus": {"type": "keyword"},
                    "cursorScoreComponents": {
                        "type": "object",
                        "properties": {
                            "acceptance_component": {"type": "float"},
                            "volume_component": {"type": "float"},
                            "chat_component": {"type": "float"},
                            "normalization_applied": {"type": "boolean"}
                        }
                    }
                }
            }
        }
        
        try:
            if self.es.indices.exists(index=index_name):
                logger.info(f"Index {index_name} already exists")
            else:
                self.es.indices.create(index=index_name, body=mapping)
                logger.info(f"Created index {index_name}")
        except Exception as e:
            logger.error(f"Error creating index {index_name}: {e}")
            raise
    
    def create_usage_events_index(self, index_name: str) -> None:
        """Create Elasticsearch index for usage events with proper mapping."""
        mapping = {
            "mappings": {
                "properties": {
                    "timestamp": {"type": "date", "format": "epoch_millis"},
                    "eventTimestamp": {"type": "date", "format": "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"},
                    "dateString": {"type": "date", "format": "yyyy-MM-dd"},
                    "date_string": {"type": "date", "format": "yyyy-MM-dd"},
                    "dateTimeString": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
                    "userEmail": {"type": "keyword"},
                    "memberName": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                    "memberRole": {"type": "keyword"},
                    "author": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                    "model": {"type": "keyword"},
                    "kind": {"type": "keyword"},
                    "maxMode": {"type": "boolean"},
                    "requestsCosts": {"type": "long"},
                    "isTokenBasedCall": {"type": "boolean"},
                    "@timestamp": {"type": "date"},
                    "ingestionDate": {"type": "date", "format": "yyyy-MM-dd"}
                }
            }
        }
        
        try:
            if self.es.indices.exists(index=index_name):
                logger.info(f"Index {index_name} already exists")
            else:
                self.es.indices.create(index=index_name, body=mapping)
                logger.info(f"Created index {index_name}")
        except Exception as e:
            logger.error(f"Error creating index {index_name}: {e}")
            raise
    
    def store_in_elasticsearch_bulk(self, enriched_data: List[Dict], index_name: str, doc_type: str = "daily") -> None:
        """Store enriched data in Elasticsearch using bulk operations."""
        if not enriched_data:
            logger.warning("No data to store")
            return
        
        logger.info(f"Storing {len(enriched_data)} records in Elasticsearch index {index_name} using bulk operations")
        
        # Create appropriate index based on document type
        if doc_type == "usage_event":
            self.create_usage_events_index(index_name)
        else:
            self.create_elasticsearch_index(index_name)
        
        # Prepare bulk data
        actions = []
        for record in enriched_data:
            doc_id = record.pop('_id')  # Remove _id from document body
            action = {
                "_index": index_name,
                "_id": doc_id,
                "_source": record
            }
            actions.append(action)
        
        # Bulk index the data in chunks
        chunk_size = 1000
        success_count = 0
        error_count = 0
        
        for i in range(0, len(actions), chunk_size):
            chunk = actions[i:i + chunk_size]
            try:
                success, failed = bulk(
                    self.es,
                    chunk,
                    index=index_name,
                    chunk_size=chunk_size,
                    request_timeout=60,
                    max_retries=3,
                    initial_backoff=2,
                    max_backoff=600
                )
                success_count += success
                error_count += len(failed) if failed else 0
                
                if failed:
                    for failure in failed:
                        logger.error(f"Bulk indexing error: {failure}")
                
                logger.info(f"Bulk indexed chunk {i//chunk_size + 1}: {success} successful")
                
            except Exception as e:
                error_count += len(chunk)
                logger.error(f"Bulk indexing chunk failed: {e}")
        
        logger.info(f"Bulk indexing complete: {success_count} successful, {error_count} errors")
    def store_in_elasticsearch(self, enriched_data: List[Dict], index_name: str) -> None:
        """Store enriched data in Elasticsearch (legacy method, use bulk for better performance)."""
        logger.warning("Using legacy single-document indexing. Consider using bulk operations.")
        self.store_in_elasticsearch_bulk(enriched_data, index_name, "daily")
    
    def run(self, start_date: datetime, end_date: datetime, 
            daily_index_name: str = "cursor-metrics", 
            events_index_name: str = "cursor-usage-events") -> None:
        """Run the complete data collection and storage process."""
        logger.info("Starting Cursor metrics collection...")
        
        # Fetch team members (shared for both operations)
        members = self.fetch_team_members()
        if not members:
            logger.error("No team members found, aborting")
            return
        
        # === DAILY USAGE DATA COLLECTION ===
        logger.info("=== Starting Daily Usage Data Collection ===")
        
        # Fetch daily usage data
        usage_data = self.fetch_daily_usage_data(start_date, end_date)
        if usage_data:
            # Enrich the data
            enriched_data = self.enrich_usage_data(usage_data, members)
            logger.info(f"Enriched {len(enriched_data)} daily usage records")
            
            # Store in Elasticsearch using bulk operations
            self.store_in_elasticsearch_bulk(enriched_data, daily_index_name, "daily")
            logger.info(f"✓ Daily usage data stored in index: {daily_index_name}")
        else:
            logger.warning("No daily usage data found")
        
        # === FILTERED USAGE EVENTS COLLECTION ===
        logger.info("=== Starting Filtered Usage Events Collection ===")
        
        # Fetch filtered usage events
        usage_events = self.fetch_filtered_usage_events(start_date, end_date)
        if usage_events:
            # Enrich the events
            enriched_events = self.enrich_usage_events(usage_events, members)
            logger.info(f"Enriched {len(enriched_events)} usage event records")
            
            # Store in Elasticsearch using bulk operations
            self.store_in_elasticsearch_bulk(enriched_events, events_index_name, "usage_event")
            logger.info(f"✓ Usage events stored in index: {events_index_name}")
        else:
            logger.warning("No usage events found")
        
        logger.info("🎉 Cursor metrics collection completed successfully!")
        
        # Generate and log score analysis if daily data was processed
        if usage_data:
            self._generate_score_analysis_report(enriched_data)
    
    def _generate_score_analysis_report(self, enriched_data: List[Dict]) -> None:
        """Generate and log a Cursor Score analysis report."""
        try:
            from cursor_score_calculator import CursorScoreAnalyzer
            
            logger.info("=== Cursor Score Analysis Report ===")
            
            # Generate distribution analysis
            analysis = CursorScoreAnalyzer.analyze_score_distribution(enriched_data)
            
            if 'error' in analysis:
                logger.warning(f"Score analysis failed: {analysis['error']}")
                return
            
            logger.info(f"Total records processed: {analysis['total_records']}")
            logger.info(f"Records with calculated scores: {analysis['calculated_scores']}")
            logger.info(f"Mean Cursor Score: {analysis['mean_score']:.2f}")
            logger.info(f"Median Cursor Score: {analysis['median_score']:.2f}")
            logger.info(f"Score range: {analysis['min_score']:.2f} - {analysis['max_score']:.2f}")
            
            logger.info("Score distribution by performance level:")
            for level, count in analysis['score_ranges'].items():
                percentage = (count / analysis['calculated_scores']) * 100 if analysis['calculated_scores'] > 0 else 0
                logger.info(f"  {level}: {count} users ({percentage:.1f}%)")
            
            # Get top performers
            top_performers = CursorScoreAnalyzer.get_top_performers(enriched_data, 5)
            if top_performers:
                logger.info("Top 5 performers:")
                for i, performer in enumerate(top_performers, 1):
                    name = performer.get('memberName', 'Unknown')
                    score = performer.get('cursorScore', 0)
                    email = performer.get('email', 'unknown')
                    logger.info(f"  {i}. {name} ({email}): {score:.2f}")
            
            logger.info("=== End of Cursor Score Analysis ===")
            
        except Exception as e:
            logger.error(f"Error generating score analysis report: {e}")


    def get_score_summary_for_date_range(self, start_date: datetime, end_date: datetime, 
                                       index_name: str = "cursor-metrics") -> Dict:
        """
        Retrieve and analyze Cursor Scores for a date range from Elasticsearch.
        
        Args:
            start_date: Start date for the query
            end_date: End date for the query
            index_name: Elasticsearch index name
            
        Returns:
            Dictionary containing score analysis
        """
        try:
            # Query Elasticsearch for the date range
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "range": {
                                    "date": {
                                        "gte": int(start_date.timestamp() * 1000),
                                        "lte": int(end_date.timestamp() * 1000)
                                    }
                                }
                            },
                            {
                                "term": {
                                    "cursorScoreStatus": "calculated"
                                }
                            }
                        ]
                    }
                },
                "size": 10000,  # Adjust based on your data size
                "_source": ["email", "memberName", "cursorScore", "cursorScoreComponents", "dateString"]
            }
            
            response = self.es.search(index=index_name, body=query)
            documents = [hit['_source'] for hit in response['hits']['hits']]
            
            if not documents:
                return {"error": "No documents found for the specified date range"}
            
            # Use the analyzer to generate statistics
            from cursor_score_calculator import CursorScoreAnalyzer
            analysis = CursorScoreAnalyzer.analyze_score_distribution(documents)
            
            return {
                "date_range": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
                "analysis": analysis,
                "sample_records": documents[:10]  # Include sample records
            }
            
        except Exception as e:
            logger.error(f"Error retrieving score summary: {e}")
            return {"error": str(e)}


def parse_date(date_str: str) -> datetime:
    """Parse date string in YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: {date_str}. Use YYYY-MM-DD")


def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(
        description='Fetch Cursor API data and store in Elasticsearch',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Run with default 1-day period (yesterday)
  python cursor_metrics.py --cursor-url https://api.cursor.com --cursor-user myuser --cursor-password mypass --es-url http://localhost:9200 --es-user elastic --es-password elastic

  # Run with custom date range
  python cursor_metrics.py --cursor-url https://api.cursor.com --cursor-user myuser --cursor-password mypass --es-url http://localhost:9200 --es-user elastic --es-password elastic --start-date 2025-01-01 --end-date 2025-01-07
        '''
    )
    
    # Cursor API arguments
    parser.add_argument('--cursor-url', required=True, help='Cursor API base URL')
    parser.add_argument('--cursor-user', required=True, help='Cursor API username')
    parser.add_argument('--cursor-password', required=True, help='Cursor API password')
    
    # Elasticsearch arguments
    parser.add_argument('--es-url', required=True, help='Elasticsearch URL')
    parser.add_argument('--es-user', required=True, help='Elasticsearch username')
    parser.add_argument('--es-password', required=True, help='Elasticsearch password')
    
    # Date range arguments
    parser.add_argument('--start-date', type=parse_date, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=parse_date, help='End date (YYYY-MM-DD)')
    parser.add_argument('--days', type=int, default=1, help='Number of days to fetch (default: 1)')
    
    # Other arguments
    parser.add_argument('--index-name', default='cursor-metrics', help='Elasticsearch index name for daily metrics')
    parser.add_argument('--events-index-name', default='cursor-usage-events', help='Elasticsearch index name for usage events')
    parser.add_argument('--users-file', default='users.txt', help='Path to users file')
    
    args = parser.parse_args()
    
    # Calculate date range
    if args.start_date and args.end_date:
        start_date = args.start_date
        end_date = args.end_date
    elif args.start_date:
        start_date = args.start_date
        end_date = start_date + timedelta(days=args.days)
    else:
        # Default to yesterday for the specified number of days
        end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = end_date - timedelta(days=args.days)
    
    logger.info(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Initialize collector
    collector = CursorMetricsCollector(
        cursor_api_url=args.cursor_url,
        cursor_auth=(args.cursor_user, args.cursor_password),
        es_url=args.es_url,
        es_auth=(args.es_user, args.es_password),
        users_file=args.users_file
    )
    
    # Run the collection
    collector.run(start_date, end_date, args.index_name, args.events_index_name)


if __name__ == "__main__":
    main()
