#!/usr/bin/env python3
"""
Script to upload a folder to Cloudflare R2 bucket.
Cloudflare R2 is S3-compatible, so we use boto3.
"""

import os
import sys
import argparse
from pathlib import Path
import boto3
from botocore.exceptions import ClientError
from tqdm import tqdm


def get_r2_client(account_id, access_key_id, secret_access_key):
    """
    Create and return an R2 client using boto3.
    
    Args:
        account_id: Cloudflare account ID
        access_key_id: R2 access key ID
        secret_access_key: R2 secret access key
    
    Returns:
        boto3 S3 client configured for R2
    """
    endpoint_url = f"https://{account_id}.r2.cloudflarestorage.com"
    
    s3_client = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        region_name='auto'  # R2 uses 'auto' as region
    )
    
    return s3_client


def upload_file(s3_client, file_path, bucket_name, object_name=None):
    """
    Upload a single file to R2 bucket.
    
    Args:
        s3_client: boto3 S3 client
        file_path: Path to file to upload
        bucket_name: Name of the R2 bucket
        object_name: S3 object name. If not specified, file_path basename is used
    
    Returns:
        True if file was uploaded, else False
    """
    if object_name is None:
        object_name = os.path.basename(file_path)
    
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
    except ClientError as e:
        print(f"Error uploading {file_path}: {e}")
        return False
    return True


def upload_folder(s3_client, folder_path, bucket_name, prefix=""):
    """
    Upload an entire folder to R2 bucket, preserving directory structure.
    
    Args:
        s3_client: boto3 S3 client
        folder_path: Path to folder to upload
        bucket_name: Name of the R2 bucket
        prefix: Prefix to prepend to object names (folder path in bucket)
    
    Returns:
        Tuple of (successful_uploads, failed_uploads)
    """
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        print(f"Error: Folder {folder_path} does not exist")
        return 0, 0
    
    if not folder_path.is_dir():
        print(f"Error: {folder_path} is not a directory")
        return 0, 0
    
    # Collect all files to upload
    files_to_upload = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = Path(root) / file
            files_to_upload.append(file_path)
    
    if not files_to_upload:
        print(f"No files found in {folder_path}")
        return 0, 0
    
    print(f"Found {len(files_to_upload)} files to upload")
    
    successful = 0
    failed = 0
    
    # Upload files with progress bar
    for file_path in tqdm(files_to_upload, desc="Uploading files"):
        # Calculate relative path from base folder
        relative_path = file_path.relative_to(folder_path)
        
        # Create object name with prefix
        if prefix:
            object_name = f"{prefix.rstrip('/')}/{relative_path}"
        else:
            object_name = str(relative_path)
        
        # Convert Windows paths to forward slashes for S3
        object_name = object_name.replace('\\', '/')
        
        if upload_file(s3_client, str(file_path), bucket_name, object_name):
            successful += 1
        else:
            failed += 1
    
    return successful, failed


def list_buckets(s3_client):
    """List all available R2 buckets."""
    try:
        response = s3_client.list_buckets()
        return [bucket['Name'] for bucket in response['Buckets']]
    except ClientError as e:
        print(f"Error listing buckets: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(
        description='Upload a folder to Cloudflare R2 bucket',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Upload results folder to bucket
  python upload_to_r2.py results my-bucket
  
  # Upload to a specific prefix (folder) in the bucket
  python upload_to_r2.py results my-bucket --prefix experiments/run1
  
  # List available buckets
  python upload_to_r2.py --list-buckets

Environment Variables:
  R2_ACCOUNT_ID          Cloudflare account ID
  R2_ACCESS_KEY_ID       R2 access key ID
  R2_SECRET_ACCESS_KEY   R2 secret access key
        """
    )
    
    parser.add_argument(
        'folder',
        nargs='?',
        help='Path to folder to upload'
    )
    parser.add_argument(
        'bucket',
        nargs='?',
        help='Name of the R2 bucket'
    )
    parser.add_argument(
        '--prefix',
        default='',
        help='Prefix (folder path) in the bucket to upload to'
    )
    parser.add_argument(
        '--account-id',
        default=os.environ.get('R2_ACCOUNT_ID'),
        help='Cloudflare account ID (or set R2_ACCOUNT_ID env var)'
    )
    parser.add_argument(
        '--access-key-id',
        default=os.environ.get('R2_ACCESS_KEY_ID'),
        help='R2 access key ID (or set R2_ACCESS_KEY_ID env var)'
    )
    parser.add_argument(
        '--secret-access-key',
        default=os.environ.get('R2_SECRET_ACCESS_KEY'),
        help='R2 secret access key (or set R2_SECRET_ACCESS_KEY env var)'
    )
    parser.add_argument(
        '--list-buckets',
        action='store_true',
        help='List available buckets and exit'
    )
    
    args = parser.parse_args()
    
    # Check credentials
    if not all([args.account_id, args.access_key_id, args.secret_access_key]):
        print("Error: Missing R2 credentials!")
        print("Please provide credentials via command line arguments or environment variables:")
        print("  --account-id or R2_ACCOUNT_ID")
        print("  --access-key-id or R2_ACCESS_KEY_ID")
        print("  --secret-access-key or R2_SECRET_ACCESS_KEY")
        sys.exit(1)
    
    # Create R2 client
    try:
        s3_client = get_r2_client(
            args.account_id,
            args.access_key_id,
            args.secret_access_key
        )
    except Exception as e:
        print(f"Error creating R2 client: {e}")
        sys.exit(1)
    
    # List buckets if requested
    if args.list_buckets:
        print("Available buckets:")
        buckets = list_buckets(s3_client)
        for bucket in buckets:
            print(f"  - {bucket}")
        sys.exit(0)
    
    # Validate arguments for upload
    if not args.folder or not args.bucket:
        print("Error: Both folder and bucket arguments are required for upload")
        parser.print_help()
        sys.exit(1)
    
    # Upload folder
    print(f"Uploading folder: {args.folder}")
    print(f"To bucket: {args.bucket}")
    if args.prefix:
        print(f"With prefix: {args.prefix}")
    print()
    
    successful, failed = upload_folder(
        s3_client,
        args.folder,
        args.bucket,
        args.prefix
    )
    
    print()
    print("=" * 50)
    print(f"Upload complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print("=" * 50)
    
    if failed > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()

