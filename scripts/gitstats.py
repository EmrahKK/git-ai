#!/usr/bin/env python3
import subprocess
import json
import time
from datetime import datetime
from collections import defaultdict
import argparse
import math
from elasticsearch import Elasticsearch, TransportError

class GitCommitAnalyzer:
    def __init__(self, args):
        self.args = args
        self.users = self.load_users()
        self.es = self.init_elasticsearch()
        self.category_weights = {
            'Refactor': 8,
            'New Work': 6,
            'Help Others': 5,
            'Churn/Rework': 4
        }
        self.refactor_threshold = 3 * 7 * 24 * 60 * 60  # 3 weeks in seconds

    def load_users(self):
        """
        Loads user mappings from the file specified by --names_input_file.
        The file should contain lines with the format:
            John Doe-U06655
            Jane Smith-U01233
            Mark Twain-U02233
        Returns a dictionary mapping lowercase author names to their alias.
        """
        users = {}
        try:
            with open(self.args.names_input_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or '-' not in line:
                        continue
                    # Split into author name and alias; trim whitespace from both parts.
                    parts = line.split('-', 1)
                    author = parts[0].strip()
                    alias = parts[1].strip()
                    users[alias] = author
            return users
        except FileNotFoundError:
            print(f"Warning: User mapping file {self.args.names_input_file} not found")
            return {}

    def init_elasticsearch(self):
        if self.args.elasticsearch_username and self.args.elasticsearch_password:
            return Elasticsearch(
                [self.args.elasticsearch_host],
                basic_auth=(self.args.elasticsearch_username, self.args.elasticsearch_password)
            )
        return Elasticsearch([self.args.elasticsearch_host])

    def run_git_command(self, cmd):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            return result.stdout.strip()
        except subprocess.SubprocessError as e:
            print(f"Git command failed: {str(e)}")
            return None

    def get_commit_details(self, commit_hash):
        """
        Retrieves details for a given commit hash using Git commands.
        Returns a dictionary with the commit hash, author name, email, date (Unix timestamp),
        commit message, and parent commit hashes.
        Also maps the author name using the user mapping (if available) so that the author
        field is replaced with the corresponding alias (e.g. U06655).
        """
        details = {
            'hash': commit_hash,
            'author': self.run_git_command(['git', 'log', '-1', '--pretty=format:%an', commit_hash]),
            'email': self.run_git_command(['git', 'log', '-1', '--pretty=format:%ae', commit_hash]),
            'date': int(self.run_git_command(['git', 'log', '-1', '--pretty=format:%ct', commit_hash])),
            'message': self.run_git_command(['git', 'log', '-1', '--pretty=format:%s', commit_hash]),
            'parents': self.run_git_command(['git', 'log', '-1', '--pretty=format:%P', commit_hash]).split(),
        }
        
        # Replace the author name with alias if it exists in the mapping.
        author = details['author'].strip() if details['author'] else ""
        if author in self.users:
            details['author'] = self.users[author]
        return details

    def get_file_stats(self, commit_hash):
        stats = []
        raw_stats = self.run_git_command(['git', 'show', '--numstat', '--pretty=', commit_hash])
        for line in raw_stats.split('\n'):
            if not line.strip():
                continue
            parts = line.split('\t')
            if len(parts) >= 3 and parts[0].isdigit() and parts[1].isdigit():
                stats.append({
                    'insertions': int(parts[0]),
                    'deletions': int(parts[1]),
                    'file': parts[2]
                })
        return stats

    def categorize_file(self, file_stat, commit_author, commit_date, commit_hash, parent_hashes):
        file_path = file_stat['file']
        insertions = file_stat['insertions']
        deletions = file_stat['deletions']

        # Get last modification info from parent commit
        last_author = None
        last_date = None
        parent_hash = parent_hashes[0] if parent_hashes else None

        if parent_hash:
            # Get last author and date for this file before current commit
            log_cmd = [
                'git', 'log', '-1', '--pretty=format:%an %ct',
                parent_hash, '--', file_path
            ]
            log_output = self.run_git_command(log_cmd)
            if log_output:
                try:
                    parts = log_output.rsplit(' ', 1)
                    last_author = parts[0].strip()
                    last_date = int(parts[1])
                except (ValueError, IndexError):
                    pass

        if not last_author or not last_date:
            # New file with no history
            return 'New Work'

        # Calculate time difference
        time_diff = commit_date - last_date

        if time_diff > self.refactor_threshold:
            total_changes = insertions + deletions
            if total_changes > 10:
                return 'Refactor'
            else:
                return 'Churn/Rework'
        else:
            if last_author != commit_author:
                return 'Help Others'
            else:
                # Check if changes are purely additive
                diff_cmd = [
                    'git', 'diff', '--unified=0',
                    parent_hash, commit_hash, '--', file_path
                ]
                diff_output = self.run_git_command(diff_cmd)
                has_additions = False
                has_deletions = False

                for line in diff_output.split('\n'):
                    if line.startswith('+') and not line.startswith('+++'):
                        has_additions = True
                    elif line.startswith('-') and not line.startswith('---'):
                        has_deletions = True

                if has_additions and not has_deletions:
                    return 'New Work'
                else:
                    return 'Churn/Rework'

    def determine_commit_category(self, counts):
        weighted = {k: counts.get(k, 0) * v for k, v in self.category_weights.items()}
        max_category = max(weighted, key=weighted.get)
        return max_category

    def calculate_efficiency(self, category, insertions, deletions):
        weights = {
            'Refactor': 0.9,
            'New Work': 0.7,
            'Help Others': 0.6,
            'Churn/Rework': 0.5
        }
        total = insertions + deletions
        if total == 0:
            return 0.0
        return round((insertions / total) * weights.get(category, 0.5)*100, 2)

    def calculate_commit_impact(self, file_stats):
        """
        Calculates the commit impact based on file changes using a logistic scaling
        to smoothly normalize the raw impact into a value between 1.0 and 100.0.
        
        Impact is computed by summing for each file:
            (insertions + deletions) * file_type_weight
        and then adding a bonus based on the number of changed files.
        
        The raw impact value is then mapped to the [1.0, 100.0] range using a logistic function.
        """
        raw_impact = 0.0

        # Define file type weights
        document_extensions = {'doc', 'docx', 'ebook', 'log', 'md', 'msg', 'odt', 'org', 'pages', 'pdf', 'rtf', 'rst', 'tex', 'txt', 'wpd', 'wps'}
        code_extensions = {'1.ada', '2.ada', 'ada', 'adb', 'ads', 'asm', 'bas', 'bash', 'bat', 'c', 'c++', 'cbl', 'cc', 'class', 'clj', 'cob', 'cpp', 'cs', 'csh', 'cxx', 'd', 'diff', 'e', 'el', 'f', 'f77', 'f90', 'fish', 'for', 'fth', 'ftn', 'go', 'groovy', 'h', 'hh', 'hpp', 'hs', 'html', 'htm', 'hxx', 'java', 'js', 'jsx', 'jsp', 'ksh', 'kt', 'lhs', 'lisp', 'lua', 'm', 'm4', 'nim', 'patch', 'php', 'pl', 'po', 'pp', 'py', 'r', 'rb', 'rs', 's', 'scala', 'sh', 'sql', 'swg', 'swift', 'v', 'vb', 'vcxproj', 'xcodeproj', 'xml', 'zsh'}
        config_extensions = {'doc', 'docx', 'ebook', 'log', 'md', 'msg', 'odt', 'org', 'pages', 'pdf', 'rtf', 'rst', 'tex', 'txt', 'wpd', 'wps'}

        for stat in file_stats:
            file_path = stat['file']
            # Get the file extension (if any)
            ext = file_path.rsplit('.', 1)[-1].lower() if '.' in file_path else ''
            if ext in document_extensions:
                weight = 0.3
            elif ext in config_extensions:
                weight = 0.7
            elif ext in code_extensions:
                weight = 0.6
            else:
                # Default weight for other file types
                weight = 0.3

            # Impact based on the sum of changes multiplied by the file weight
            #file_impact = (stat['insertions'] + stat['deletions']) * weight
            file_impact = (stat['insertions'] + stat['deletions']) * weight
            raw_impact += file_impact

        # Additionally, incorporate the number of changed files to increase impact
        raw_impact += len(file_stats)*raw_impact

        # Normalize raw impact using a logistic (sigmoid) function.
        # The logistic function maps the raw impact (which is unbounded) smoothly to [1.0, 100.0].
        #
        # We'll use a formulation:
        #     normalized = lower_bound + (upper_bound - lower_bound) / (1 + exp(-k*(raw_impact - x0)))
        #
        # where:
        #     - lower_bound = 1.0 and upper_bound = 100.0,
        #     - k controls the steepness of the curve,
        #     - x0 is the midpoint of the raw impact scale.
        #
        # Adjust k and x0 based on the expected range of raw_impact in your repository.
        lower_bound = 1.0
        upper_bound = 100.0
        k = 0.01  # steepness parameter (adjust as needed)
        x0 = 500.0  # midpoint parameter (adjust as needed)

        # Compute the logistic function value.
        normalized = lower_bound + (upper_bound - lower_bound) / (1 + math.exp(-k * (raw_impact - x0)))
        return round(normalized, 1)

    def process_commit(self, commit_hash):
        details = self.get_commit_details(commit_hash)
        if len(details['parents']) >= 2:
            return None  # Skip merge commits

        file_stats = self.get_file_stats(commit_hash)
        if not file_stats:
            return None

        category_counts = defaultdict(int)
        for stat in file_stats:
            category = self.categorize_file(
                stat,
                details['author'],
                details['date'],
                commit_hash,
                details['parents']
            )
            category_counts[category] += 1

        commit_category = self.determine_commit_category(category_counts)
        total_insertions = sum(s['insertions'] for s in file_stats)
        total_deletions = sum(s['deletions'] for s in file_stats)

        doc = {
            'sha': commit_hash,
            'author': details['author'],
            'email': details['email'],
            'commit_date': details['date'],
            'date': datetime.fromtimestamp(details['date']).isoformat(),
            'dateString': datetime.fromtimestamp(details['date']).isoformat(),
            'message': details['message'],
            'project_name': self.args.project_name,
            'repository_name': self.args.repository_name,
            'total_files_changed': len(file_stats),
            'insertions': total_insertions,
            'deletions': total_deletions,
            'category': commit_category,
            'cefficiency': self.calculate_efficiency(commit_category, total_insertions, total_deletions),
            'commit_impact': self.calculate_commit_impact(file_stats),
            'files': file_stats
        }

        return doc

    def send_to_elasticsearch(self, doc):
        # print(f"index document {doc}")
        # print(f"###")
        # time.sleep(0.1)
        try:
            self.es.index(
                index=self.args.index_name,
                id=doc['sha'],
                document=doc
            )
            time.sleep(0.1)
        except TransportError as e:
            print(f"Failed to index document {doc['sha']}: {str(e)}")

    def run(self):
        commits = self.run_git_command([
            'git', 'log',
            '--since', self.args.since,
            '--until', self.args.until,
            '--pretty=format:%H'
        ]).split()
        
        print(f"Found {len(commits)} commits, between {self.args.until} - {self.args.since}")
        
        for commit_hash in commits:
            doc = self.process_commit(commit_hash)
            if doc:
                self.send_to_elasticsearch(doc)
                print(f"Processed commit {commit_hash[:6]} ({doc['category']})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze Git commits and send to Elasticsearch')
    parser.add_argument('--since', default='3 week ago', help='Time range start')
    parser.add_argument('--until', default='now', help='Time range end')
    parser.add_argument('--project_name', required=True, help='Project name')
    parser.add_argument('--repository_name', required=True, help='Repository name')
    parser.add_argument('--elasticsearch_host', default='http://localhost:9200', help='Elasticsearch host URL')
    parser.add_argument('--index_name', default='git-stats-combined', help='Elasticsearch index name')
    parser.add_argument('--elasticsearch_username', help='Elasticsearch username')
    parser.add_argument('--elasticsearch_password', help='Elasticsearch password')
    parser.add_argument('--names_input_file', default='users.txt', help='User mapping file')

    args = parser.parse_args()
    
    analyzer = GitCommitAnalyzer(args)
    analyzer.run()

