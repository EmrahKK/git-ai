#!/usr/bin/env python3
"""
DORA Metrics Data Pipeline Script
Fetches data from MS SQL Server and indexes it into Elasticsearch for DORA metrics dashboard.
Enriches documents with team information from teams.txt file.

Usage:
python dora_pipeline.py --elasticsearch-url http://localhost:9200 \
                        --elasticsearch-user elastic \
                        --elasticsearch-password password \
                        --days 30 \
                        --db-host localhost \
                        --db-port 1433 \
                        --db-name your-database \
                        --db-username username \
                        --db-password password \
                        --teams-file teams.txt
"""

import argparse
import sys
import hashlib
import logging
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Set
import pyodbc
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DORAMetricsPipeline:
    def __init__(self, args):
        self.args = args
        self.es_client = None
        self.db_connection = None
        self.teams_mapping = {}  # Will store developer name -> team name mapping
        
        # Index names
        self.deployment_frequency_index = "dora-deployment-frequency"
        self.lead_time_index = "dora-lead-time"
        
        # Index mappings (updated to include team and product fields)
        self.deployment_frequency_mapping = {
            "mappings": {
                "properties": {
                    "project_name": {"type": "keyword"},
                    "tfs_build_id": {"type": "keyword"},
                    "release_date": {"type": "date"},
                    "release_status": {"type": "keyword"},
                    "created_by_name": {"type": "keyword"},
                    "author": {"type": "keyword"},
                    "created_by_registration": {"type": "keyword"},
                    "products": {"type": "text"},
                    "unique_id": {"type": "keyword"},
                    "is_hotfix": {"type": "boolean"},
                    "date_string": {"type": "date"},
                    "ingestion_timestamp": {"type": "date"},
                    "team": {"type": "keyword"},  # Team field
                    "product": {"type": "keyword"},  # Clean product field
                    "products_cleaned": {"type": "boolean"}  # Flag to indicate products were processed
                }
            }
        }
        
        self.lead_time_mapping = {
            "mappings": {
                "properties": {
                    "tfs_build_id": {"type": "keyword"},
                    "project_name": {"type": "keyword"},
                    "repository": {"type": "keyword"},
                    "pull_request_id": {"type": "keyword"},
                    "first_commit_date": {"type": "date"},
                    "deployment_date": {"type": "date"},
                    "pushed_by_name": {"type": "keyword"},
                    "author": {"type": "keyword"},
                    "pushed_by_registration": {"type": "keyword"},
                    "commit_to_deploy_time": {"type": "keyword"},
                    "lead_time_minutes": {"type": "long"},
                    "lead_time_hours": {"type": "float"},
                    "lead_time_days": {"type": "float"},
                    "products": {"type": "text"},
                    "date_string": {"type": "date"},
                    "ingestion_timestamp": {"type": "date"},
                    "team": {"type": "keyword"},  # Team field
                    "product": {"type": "keyword"},  # Clean product field
                    "products_cleaned": {"type": "boolean"}  # Flag to indicate products were processed
                }
            }
        }

    def load_teams_mapping(self) -> bool:
        """Load teams mapping from teams.txt file"""
        try:
            if not self.args.teams_file:
                logger.warning("No teams file specified. Team field will be set to 'Non' for all documents.")
                return True
                
            if not os.path.exists(self.args.teams_file):
                logger.error(f"Teams file not found: {self.args.teams_file}")
                return False
            
            teams_count = 0
            with open(self.args.teams_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Split by the last occurrence of '-' to handle team names with dashes
                    if '-' in line:
                        parts = line.rsplit('-', 1)
                        if len(parts) == 2:
                            team_name = parts[0].strip()
                            developer_name = parts[1].strip()
                            
                            if team_name and developer_name:
                                self.teams_mapping[developer_name] = team_name
                                teams_count += 1
                            else:
                                logger.warning(f"Line {line_num}: Empty team or developer name in '{line}'")
                        else:
                            logger.warning(f"Line {line_num}: Invalid format '{line}' - expected format: 'Team Name-Developer Name'")
                    else:
                        logger.warning(f"Line {line_num}: No delimiter '-' found in '{line}'")
            
            logger.info(f"Loaded {teams_count} developer-team mappings from {self.args.teams_file}")
            
            # Log some examples for verification
            if teams_count > 0:
                logger.info("Sample mappings:")
                for i, (dev, team) in enumerate(list(self.teams_mapping.items())[:5]):
                    logger.info(f"  - {dev} -> {team}")
                if teams_count > 5:
                    logger.info(f"  ... and {teams_count - 5} more")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading teams mapping: {str(e)}")
            return False

    def get_team_for_developer(self, developer_name: str) -> str:
        """Get team name for a developer, return 'Non' if not found"""
        if not developer_name:
            return "Non"
        
        # Try exact match first
        if developer_name in self.teams_mapping:
            return self.teams_mapping[developer_name]
        
        # Try case-insensitive match
        for dev_name, team_name in self.teams_mapping.items():
            if dev_name.lower() == developer_name.lower():
                return team_name
        
        # If no match found
        return "Non"

    def extract_products_from_string(self, products_string: str) -> List[str]:
        """
        Extract unique, clean product names from the messy products string.
        
        Examples:
        "0#ÜRÜN_MEVDUAT ÜRÜNLERİ(91495)" -> ["MEVDUAT ÜRÜNLERİ"]
        "0#ÜRÜN_KREDİ KARTI(188729)" -> ["KREDİ KARTI"]
        "0#() " -> []
        "0#ÜRÜN_KREDİ KARTI(188729) #ÜRÜN_KREDİ KARTI(188729)" -> ["KREDİ KARTI"]
        """
        if not products_string or products_string.strip() == "":
            return ["non"]
        
        line = products_string.strip()
        
        # Use the improved regex pattern that captures product name even if it contains parentheses
        pattern = r'#ÜRÜN_(.+?)\(\d+\)'
        
        # Find all matches
        matches = re.findall(pattern, line)
        
        if matches:
            # Clean the matches and remove duplicates while preserving order
            seen = set()
            unique_products = []
            
            for match in matches:
                cleaned = match.strip()
                if cleaned and cleaned not in seen:
                    unique_products.append(cleaned)
                    seen.add(cleaned)
            
            return unique_products
        else:
            # Check if it's just empty tags like "#()"
            if re.search(r'#\s*\(.*?\)', line):
                return ["non"]  # Return ["non"] for empty tags
            else:
                return ["non"]

    def create_standardized_products_string(self, product_list: List[str]) -> str:
        """Create a clean, standardized products string"""
        if not product_list:
            return "non"
        
        # Filter out "non" entries if there are other valid products
        filtered_products = [p for p in product_list if p != "non"]
        
        if not filtered_products:
            return "non"
        
        # Create standardized format: comma-separated, clean names
        return ", ".join(filtered_products)

    def process_products_field(self, products_string: str) -> str:
        """Process products field and return clean product string"""
        clean_products_list = self.extract_products_from_string(products_string)
        return self.create_standardized_products_string(clean_products_list)

    def connect_elasticsearch(self) -> bool:
        """Connect to Elasticsearch cluster"""
        try:
            if self.args.elasticsearch_user and self.args.elasticsearch_password:
                self.es_client = Elasticsearch(
                    [self.args.elasticsearch_url],
                    http_auth=(self.args.elasticsearch_user, self.args.elasticsearch_password),
                    verify_certs=False,
                    timeout=30
                )
            else:
                self.es_client = Elasticsearch(
                    [self.args.elasticsearch_url],
                    verify_certs=False,
                    timeout=30
                )
            
            # Test connection
            if self.es_client.ping():
                logger.info(f"Connected to Elasticsearch at {self.args.elasticsearch_url}")
                return True
            else:
                logger.error("Failed to connect to Elasticsearch")
                return False
                
        except Exception as e:
            logger.error(f"Elasticsearch connection error: {str(e)}")
            return False

    def connect_database(self) -> bool:
        """Connect to MS SQL Server database"""
        try:
            # Try Microsoft ODBC Driver first, fallback to FreeTDS
            connection_strings = [
                # Microsoft ODBC Driver 17
                (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={self.args.db_host},{self.args.db_port};"
                    f"DATABASE={self.args.db_name};"
                    f"UID={self.args.db_username};"
                    f"PWD={self.args.db_password};"
                    f"TrustServerCertificate=yes;"
                ),
                # Microsoft ODBC Driver 18
                (
                    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                    f"SERVER={self.args.db_host},{self.args.db_port};"
                    f"DATABASE={self.args.db_name};"
                    f"UID={self.args.db_username};"
                    f"PWD={self.args.db_password};"
                    f"TrustServerCertificate=yes;"
                ),
                # FreeTDS Driver
                (
                    f"DRIVER={{FreeTDS}};"
                    f"SERVER={self.args.db_host};"
                    f"PORT={self.args.db_port};"
                    f"DATABASE={self.args.db_name};"
                    f"UID={self.args.db_username};"
                    f"PWD={self.args.db_password};"
                    f"TDS_Version=8.0;"
                )
            ]
            
            connection_exception = None
            for connection_string in connection_strings:
                try:
                    self.db_connection = pyodbc.connect(connection_string)
                    logger.info(f"Connected to SQL Server database: {self.args.db_name} with one of the available drivers.")
                    return True  # Exit after successful connection
                except Exception as e:
                    connection_exception = e
                    logger.warning(f"Connection attempt failed with one of the drivers. Trying next...")
                    continue # This continue is now part of the correct logic
            
            # If the loop finishes, it means all connections failed.
            if connection_exception:
                logger.error(f"Database connection error: {str(connection_exception)}")

            return False
            
        except Exception as e:
            logger.error(f"Database connection error: {str(e)}")
            return False

    def create_indices(self):
        """Create Elasticsearch indices with proper mappings"""
        try:
            # Create deployment frequency index
            if not self.es_client.indices.exists(index=self.deployment_frequency_index):
                self.es_client.indices.create(
                    index=self.deployment_frequency_index,
                    **self.deployment_frequency_mapping
                )
                logger.info(f"Created index: {self.deployment_frequency_index}")
            
            # Create lead time index
            if not self.es_client.indices.exists(index=self.lead_time_index):
                self.es_client.indices.create(
                    index=self.lead_time_index,
                    **self.lead_time_mapping
                )
                logger.info(f"Created index: {self.lead_time_index}")
                
        except Exception as e:
            logger.error(f"Error creating indices: {str(e)}")
            raise

    def generate_unique_id(self, fields: List[str]) -> str:
        """Generate unique ID from multiple fields using SHA256"""
        combined_string = "-".join(str(field) for field in fields)
        return hashlib.sha256(combined_string.encode()).hexdigest()[:16]

    def parse_duration_to_minutes(self, duration_str: str) -> Optional[float]:
        """Parse duration string (HH:MM:SS.mmmmmmm) to total minutes"""
        try:
            if not duration_str:
                return None
            
            parts = duration_str.split(':')
            if len(parts) < 3:
                return None
            
            hours = float(parts[0])
            minutes = float(parts[1])
            seconds = float(parts[2])
            
            total_minutes = (hours * 60) + minutes + (seconds / 60)
            return round(total_minutes, 2)
            
        except Exception as e:
            logger.warning(f"Error parsing duration '{duration_str}': {str(e)}")
            return None

    def fetch_release_frequency_data(self) -> List[Dict[str, Any]]:
        """Fetch data from ReleaseFrequencyNew table"""
        try:
            # Use specific days for this table if provided, otherwise use default
            days_to_fetch = self.args.release_days if self.args.release_days else self.args.days
            
            if self.args.all_data:
                # Fetch all data without date filtering
                query = """
                SELECT ID, ProjectName, TfsBuildID, ReleaseDate, ReleaseStatus, 
                       CreatedByName, CreatedByRegistration, Products, UniqID, Hotfix
                FROM ReleaseFrequencyNew 
                WHERE ReleaseDate IS NOT NULL AND ReleaseDate != ''
                ORDER BY CONVERT(datetime, ReleaseDate, 101) DESC
                """
                logger.info("Querying ALL ReleaseFrequencyNew data (no date filter)")
                
                cursor = self.db_connection.cursor()
                cursor.execute(query)
            else:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days_to_fetch)
                
                # Format dates for SQL Server in MM/DD/YYYY HH:MM:SS format to match your data
                start_date_str = start_date.strftime('%m/%d/%Y %H:%M:%S')
                end_date_str = end_date.strftime('%m/%d/%Y %H:%M:%S')
                
                # First, let's check the actual date range in the table
                cursor = self.db_connection.cursor()
                
                # Get the date range of available data
                cursor.execute("""
                    SELECT MIN(CONVERT(datetime, ReleaseDate, 101)) as min_date, 
                           MAX(CONVERT(datetime, ReleaseDate, 101)) as max_date,
                           COUNT(*) as total_count
                    FROM ReleaseFrequencyNew 
                    WHERE ReleaseDate IS NOT NULL AND ReleaseDate != ''
                """)
                date_info = cursor.fetchone()
                if date_info:
                    logger.info(f"ReleaseFrequencyNew date range: {date_info[0]} to {date_info[1]} (Total: {date_info[2]} records)")
                    
                    # If no data in our date range, show some sample recent data
                    if date_info[2] > 0:
                        cursor.execute("""
                            SELECT TOP 5 ProjectName, ReleaseDate, ReleaseStatus 
                            FROM ReleaseFrequencyNew 
                            ORDER BY CONVERT(datetime, ReleaseDate, 101) DESC
                        """)
                        samples = cursor.fetchall()
                        logger.info("Most recent ReleaseFrequencyNew records:")
                        for sample in samples:
                            logger.info(f"  - {sample[0]}: {sample[1]} ({sample[2]})")
                
                # Now query with date range
                query = """
                SELECT ID, ProjectName, TfsBuildID, ReleaseDate, ReleaseStatus, 
                       CreatedByName, CreatedByRegistration, Products, UniqID, Hotfix
                FROM ReleaseFrequencyNew 
                WHERE CONVERT(datetime, ReleaseDate, 101) >= CONVERT(datetime, ?, 101) 
                AND CONVERT(datetime, ReleaseDate, 101) <= CONVERT(datetime, ?, 101)
                ORDER BY CONVERT(datetime, ReleaseDate, 101) DESC
                """
                
                logger.info(f"Querying ReleaseFrequencyNew from {start_date_str} to {end_date_str} ({days_to_fetch} days)")
                cursor.execute(query, start_date_str, end_date_str)
            
            columns = [column[0] for column in cursor.description]
            data = []
            team_stats = {}  # Track team distribution
            product_stats = {}  # Track product distribution
            
            for row in cursor.fetchall():
                row_dict = dict(zip(columns, row))
                
                # Handle ReleaseDate - convert to datetime if it's a string
                release_date = row_dict.get('ReleaseDate', '')
                if isinstance(release_date, str):
                    try:
                        # Parse MM/DD/YYYY HH:MM:SS format
                        release_date = datetime.strptime(release_date, '%m/%d/%Y %H:%M:%S')
                    except ValueError:
                        try:
                            # Try other common formats as fallback
                            for date_format in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f']:
                                try:
                                    release_date = datetime.strptime(release_date, date_format)
                                    break
                                except ValueError:
                                    continue
                            else:
                                # If no format worked, try parsing with dateutil
                                from dateutil import parser
                                release_date = parser.parse(release_date)
                        except Exception as e:
                            logger.warning(f"Could not parse date '{release_date}': {e}")
                            release_date = None
                
                # Get team for developer
                created_by_name = row_dict.get('CreatedByName', '')
                team = self.get_team_for_developer(created_by_name)
                
                # Process products field
                products_raw = row_dict.get('Products', '')
                product_clean = self.process_products_field(products_raw)
                
                # Track statistics
                team_stats[team] = team_stats.get(team, 0) + 1
                product_stats[product_clean] = product_stats.get(product_clean, 0) + 1
                
                # Generate unique document ID
                unique_fields = [
                    row_dict.get('ProjectName', ''),
                    row_dict.get('TfsBuildID', ''),
                    row_dict.get('UniqID', ''),
                    release_date.strftime('%Y-%m-%d %H:%M:%S') if release_date else ''
                ]
                doc_id = self.generate_unique_id(unique_fields)
                
                # Transform data for Elasticsearch
                doc = {
                    "_id": doc_id,
                    "project_name": row_dict.get('ProjectName', ''),
                    "tfs_build_id": str(row_dict.get('TfsBuildID', '')),
                    "release_date": release_date,
                    "release_status": row_dict.get('ReleaseStatus', ''),
                    "created_by_name": created_by_name,
                    "author": created_by_name,
                    "created_by_registration": row_dict.get('CreatedByRegistration', ''),
                    "products": products_raw,
                    "unique_id": row_dict.get('UniqID', ''),
                    "is_hotfix": bool(row_dict.get('Hotfix', 0)),
                    "date_string": release_date,
                    "ingestion_timestamp": datetime.now(),
                    "team": team,  # Team field
                    "product": product_clean,  # Clean product field
                    "products_cleaned": True  # Flag to indicate processing
                }
                
                data.append(doc)
            
            logger.info(f"Fetched {len(data)} records from ReleaseFrequencyNew table")
            
            # Log team distribution
            if team_stats:
                logger.info("Team distribution for deployment frequency:")
                for team, count in sorted(team_stats.items(), key=lambda x: x[1], reverse=True):
                    logger.info(f"  - {team}: {count} deployments")
            
            # Log product distribution (top 10)
            if product_stats:
                logger.info("Top 10 products for deployment frequency:")
                sorted_products = sorted(product_stats.items(), key=lambda x: x[1], reverse=True)[:10]
                for product, count in sorted_products:
                    logger.info(f"  - {product}: {count} deployments")
            
            # If no data found and not fetching all data, suggest alternatives
            if len(data) == 0 and not self.args.all_data:
                logger.warning(f"No ReleaseFrequencyNew data found in the specified date range")
                logger.warning(f"Try using --all-data flag to fetch all available data, or --release-days with a larger number")
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching release frequency data: {str(e)}")
            raise

    def fetch_lead_time_data(self) -> List[Dict[str, Any]]:
        """Fetch data from LeadTimeForChangeTFS table"""
        try:
            # Use specific days for this table if provided, otherwise use default
            days_to_fetch = self.args.leadtime_days if self.args.leadtime_days else self.args.days
            
            if self.args.all_data:
                # Fetch all data without date filtering
                query = """
                SELECT Id, TfsBuildID, ProjectName, Repository, PullRequestId, 
                       FirstCommitDate, DeploymentDate, PushedByName, PushedByRegistration, 
                       CommitToDeployTime, Products
                FROM LeadTimeForChangeTFS 
                WHERE DeploymentDate IS NOT NULL AND DeploymentDate != ''
                ORDER BY CONVERT(datetime, DeploymentDate, 101) DESC
                """
                logger.info("Querying ALL LeadTimeForChangeTFS data (no date filter)")
                
                cursor = self.db_connection.cursor()
                cursor.execute(query)
            else:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days_to_fetch)
                
                # Format dates for SQL Server in MM/DD/YYYY HH:MM:SS format to match your data
                start_date_str = start_date.strftime('%m/%d/%Y %H:%M:%S')
                end_date_str = end_date.strftime('%m/%d/%Y %H:%M:%S')
                
                # First, let's check the actual date range in the table
                cursor = self.db_connection.cursor()
                
                # Get the date range of available data
                cursor.execute("""
                    SELECT MIN(CONVERT(datetime, DeploymentDate, 101)) as min_date, 
                           MAX(CONVERT(datetime, DeploymentDate, 101)) as max_date,
                           COUNT(*) as total_count
                    FROM LeadTimeForChangeTFS 
                    WHERE DeploymentDate IS NOT NULL AND DeploymentDate != ''
                """)
                date_info = cursor.fetchone()
                if date_info:
                    logger.info(f"LeadTimeForChangeTFS date range: {date_info[0]} to {date_info[1]} (Total: {date_info[2]} records)")
                    
                    # If no data in our date range, show some sample recent data
                    if date_info[2] > 0:
                        cursor.execute("""
                            SELECT TOP 5 ProjectName, DeploymentDate, CommitToDeployTime 
                            FROM LeadTimeForChangeTFS 
                            ORDER BY CONVERT(datetime, DeploymentDate, 101) DESC
                        """)
                        samples = cursor.fetchall()
                        logger.info("Most recent LeadTimeForChangeTFS records:")
                        for sample in samples:
                            logger.info(f"  - {sample[0]}: {sample[1]} (Lead time: {sample[2]})")
                
                # Now query with date range
                query = """
                SELECT Id, TfsBuildID, ProjectName, Repository, PullRequestId, 
                       FirstCommitDate, DeploymentDate, PushedByName, PushedByRegistration, 
                       CommitToDeployTime, Products
                FROM LeadTimeForChangeTFS 
                WHERE CONVERT(datetime, DeploymentDate, 101) >= CONVERT(datetime, ?, 101) 
                AND CONVERT(datetime, DeploymentDate, 101) <= CONVERT(datetime, ?, 101)
                ORDER BY CONVERT(datetime, DeploymentDate, 101) DESC
                """
                
                logger.info(f"Querying LeadTimeForChangeTFS from {start_date_str} to {end_date_str} ({days_to_fetch} days)")
                cursor.execute(query, start_date_str, end_date_str)
            
            columns = [column[0] for column in cursor.description]
            data = []
            team_stats = {}  # Track team distribution
            product_stats = {}  # Track product distribution
            
            for row in cursor.fetchall():
                row_dict = dict(zip(columns, row))
                
                # Handle date fields - convert to datetime if they're strings
                def parse_date_field(date_value):
                    if isinstance(date_value, str):
                        try:
                            # Parse MM/DD/YYYY HH:MM:SS format first
                            return datetime.strptime(date_value, '%m/%d/%Y %H:%M:%S')
                        except ValueError:
                            try:
                                # Try other formats as fallback
                                for date_format in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f']:
                                    try:
                                        return datetime.strptime(date_value, date_format)
                                    except ValueError:
                                        continue
                                # If no format worked, try parsing with dateutil
                                from dateutil import parser
                                return parser.parse(date_value)
                            except Exception as e:
                                logger.warning(f"Could not parse date '{date_value}': {e}")
                                return None
                    return date_value
                
                first_commit_date = parse_date_field(row_dict.get('FirstCommitDate', ''))
                deployment_date = parse_date_field(row_dict.get('DeploymentDate', ''))
                
                # Get team for developer
                pushed_by_name = row_dict.get('PushedByName', '')
                team = self.get_team_for_developer(pushed_by_name)
                
                # Process products field
                products_raw = row_dict.get('Products', '')
                product_clean = self.process_products_field(products_raw)
                
                # Track statistics
                team_stats[team] = team_stats.get(team, 0) + 1
                product_stats[product_clean] = product_stats.get(product_clean, 0) + 1
                
                # Generate unique document ID
                unique_fields = [
                    row_dict.get('TfsBuildID', ''),
                    row_dict.get('ProjectName', ''),
                    row_dict.get('Repository', ''),
                    row_dict.get('PullRequestId', ''),
                    deployment_date.strftime('%Y-%m-%d %H:%M:%S') if deployment_date else ''
                ]
                doc_id = self.generate_unique_id(unique_fields)
                
                # Parse lead time duration
                duration_str = row_dict.get('CommitToDeployTime', '')
                lead_time_minutes = self.parse_duration_to_minutes(duration_str)
                
                # Transform data for Elasticsearch
                doc = {
                    "_id": doc_id,
                    "tfs_build_id": str(row_dict.get('TfsBuildID', '')),
                    "project_name": row_dict.get('ProjectName', ''),
                    "repository": row_dict.get('Repository', ''),
                    "pull_request_id": str(row_dict.get('PullRequestId', '')),
                    "first_commit_date": first_commit_date,
                    "deployment_date": deployment_date,
                    "pushed_by_name": pushed_by_name,
                    "author": pushed_by_name,
                    "pushed_by_registration": row_dict.get('PushedByRegistration', ''),
                    "commit_to_deploy_time": duration_str,
                    "lead_time_minutes": lead_time_minutes,
                    "lead_time_hours": round(lead_time_minutes / 60, 2) if lead_time_minutes else None,
                    "lead_time_days": round(lead_time_minutes / 1440, 2) if lead_time_minutes else None,
                    "products": products_raw,
                    "date_string": deployment_date,
                    "ingestion_timestamp": datetime.now(),
                    "team": team,  # Team field
                    "product": product_clean,  # Clean product field
                    "products_cleaned": True  # Flag to indicate processing
                }
                
                data.append(doc)
            
            logger.info(f"Fetched {len(data)} records from LeadTimeForChangeTFS table")
            
            # Log team distribution
            if team_stats:
                logger.info("Team distribution for lead time:")
                for team, count in sorted(team_stats.items(), key=lambda x: x[1], reverse=True):
                    logger.info(f"  - {team}: {count} changes")
            
            # Log product distribution (top 10)
            if product_stats:
                logger.info("Top 10 products for lead time:")
                sorted_products = sorted(product_stats.items(), key=lambda x: x[1], reverse=True)[:10]
                for product, count in sorted_products:
                    logger.info(f"  - {product}: {count} changes")
            
            # If no data found and not fetching all data, suggest alternatives
            if len(data) == 0 and not self.args.all_data:
                logger.warning(f"No LeadTimeForChangeTFS data found in the specified date range")
                logger.warning(f"Try using --all-data flag to fetch all available data, or --leadtime-days with a larger number")
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching lead time data: {str(e)}")
            raise

    def bulk_index_documents(self, index_name: str, documents: List[Dict[str, Any]]) -> bool:
        """Bulk index documents to Elasticsearch"""
        try:
            if not documents:
                logger.warning(f"No documents to index for {index_name}")
                return True
            
            # Prepare documents for bulk indexing
            actions = []
            for doc in documents:
                action = {
                    "_index": index_name,
                    "_id": doc["_id"],
                    "_source": {k: v for k, v in doc.items() if k != "_id"}
                }
                actions.append(action)
            
            # Perform bulk indexing
            success_count, failed_items = bulk(
                self.es_client,
                actions,
                chunk_size=500,
                request_timeout=60
            )
            
            logger.info(f"Successfully indexed {success_count} documents to {index_name}")
            
            if failed_items:
                logger.warning(f"Failed to index {len(failed_items)} documents to {index_name}")
                for item in failed_items[:5]:  # Log first 5 failures
                    logger.warning(f"Failed item: {item}")
            
            return len(failed_items) == 0
            
        except Exception as e:
            logger.error(f"Error bulk indexing to {index_name}: {str(e)}")
            return False

    def run(self) -> bool:
        """Main execution method"""
        try:
            logger.info("Starting DORA Metrics Data Pipeline with Team and Product Enrichment")
            logger.info(f"Processing data for the last {self.args.days} days")
            
            # Load teams mapping
            if not self.load_teams_mapping():
                return False
            
            # Connect to services
            if not self.connect_elasticsearch():
                return False
            
            if not self.connect_database():
                return False
            
            # Create indices
            self.create_indices()
            
            # Process ReleaseFrequencyNew data
            logger.info("Processing ReleaseFrequencyNew data...")
            release_data = self.fetch_release_frequency_data()
            if not self.bulk_index_documents(self.deployment_frequency_index, release_data):
                logger.error("Failed to index release frequency data")
                return False
            
            # Process LeadTimeForChangeTFS data
            logger.info("Processing LeadTimeForChangeTFS data...")
            lead_time_data = self.fetch_lead_time_data()
            if not self.bulk_index_documents(self.lead_time_index, lead_time_data):
                logger.error("Failed to index lead time data")
                return False
            
            logger.info("DORA Metrics Data Pipeline completed successfully")
            logger.info("Documents now include:")
            logger.info("  - 'team' field: Team assignment for each developer")
            logger.info("  - 'product' field: Clean, standardized product names")
            logger.info("  - 'products_cleaned' field: Flag indicating products were processed")
            return True
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {str(e)}")
            return False
        
        finally:
            # Clean up connections
            if self.db_connection:
                self.db_connection.close()


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="DORA Metrics Data Pipeline - Fetch data from MS SQL and index to Elasticsearch with team enrichment"
    )
    
    # Elasticsearch parameters
    parser.add_argument(
        "--elasticsearch-url",
        required=True,
        help="Elasticsearch URL (e.g., http://localhost:9200)"
    )
    parser.add_argument(
        "--elasticsearch-user",
        help="Elasticsearch username (optional)"
    )
    parser.add_argument(
        "--elasticsearch-password",
        help="Elasticsearch password (optional)"
    )
    
    # Database parameters
    parser.add_argument(
        "--db-host",
        required=True,
        help="Database host"
    )
    parser.add_argument(
        "--db-port",
        type=int,
        default=1433,
        help="Database port (default: 1433)"
    )
    parser.add_argument(
        "--db-name",
        required=True,
        help="Database name"
    )
    parser.add_argument(
        "--db-username",
        required=True,
        help="Database username"
    )
    parser.add_argument(
        "--db-password",
        required=True,
        help="Database password"
    )
    
    # Teams file parameter
    parser.add_argument(
        "--teams-file",
        default="teams.txt",
        help="Path to teams mapping file (default: teams.txt)"
    )
    
    # Processing parameters
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Number of days to fetch data for (default: 30)"
    )
    parser.add_argument(
        "--release-days",
        type=int,
        help="Number of days to fetch ReleaseFrequencyNew data for (overrides --days for this table)"
    )
    parser.add_argument(
        "--leadtime-days",
        type=int,
        help="Number of days to fetch LeadTimeForChangeTFS data for (overrides --days for this table)"
    )
    parser.add_argument(
        "--all-data",
        action="store_true",
        help="Fetch all available data regardless of date range"
    )
    
    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_arguments()
    
    pipeline = DORAMetricsPipeline(args)
    success = pipeline.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()