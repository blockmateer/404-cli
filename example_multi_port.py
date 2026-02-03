#!/usr/bin/env python3
"""
Example: Using Generator with Multi-Port Load Balancing

This example demonstrates how to use the Generator class with multiple
endpoints for load balancing across 4 GPUs.
"""

import asyncio
from pathlib import Path
from generator import Generator


async def main():
    """Main example function"""
    
    # ========================================================================
    # EXAMPLE 1: Single Endpoint (Traditional)
    # ========================================================================
    print("=" * 70)
    print("Example 1: Single Endpoint")
    print("=" * 70)
    
    single_endpoint = "http://0.0.0.0:10006"
    
    generator_single = Generator(
        endpoint=single_endpoint,
        seed=42,
        output_folder=Path("./output_single"),
        echo=print
    )
    
    print()
    
    # ========================================================================
    # EXAMPLE 2: Multi-Port with 4 GPUs (Recommended)
    # ========================================================================
    print("=" * 70)
    print("Example 2: Multi-Port with 4 GPUs")
    print("=" * 70)
    
    multi_endpoints = [
        "http://0.0.0.0:10006",  # GPU 0
        "http://0.0.0.0:10007",  # GPU 1
        "http://0.0.0.0:10008",  # GPU 2
        "http://0.0.0.0:10009",  # GPU 3
    ]
    
    generator_multi = Generator(
        endpoint=multi_endpoints,
        seed=42,
        output_folder=Path("./output_multi"),
        echo=print
    )
    
    print()
    
    # ========================================================================
    # EXAMPLE 3: Process Multiple Images
    # ========================================================================
    print("=" * 70)
    print("Example 3: Processing Multiple Images")
    print("=" * 70)
    
    # Example image URLs (replace with your actual URLs)
    image_urls = [
        "https://example.com/image1.png",
        "https://example.com/image2.png",
        "https://example.com/image3.png",
        "https://example.com/image4.png",
        "https://example.com/image5.png",
        "https://example.com/image6.png",
        "https://example.com/image7.png",
        "https://example.com/image8.png",
    ]
    
    print(f"Processing {len(image_urls)} images...")
    print(f"With multi-port setup, these will be distributed across 4 GPUs")
    print(f"Expected time: ~{len(image_urls) * 45 / 4 / 60:.1f} minutes (vs {len(image_urls) * 45 / 60:.1f} minutes with single GPU)")
    print()
    
    # Uncomment to actually run:
    # await generator_multi.generate_all(image_urls)
    
    # ========================================================================
    # EXAMPLE 4: Custom Configuration (2 GPUs only)
    # ========================================================================
    print("=" * 70)
    print("Example 4: Using Only 2 GPUs")
    print("=" * 70)
    
    two_gpu_endpoints = [
        "http://0.0.0.0:10006",  # GPU 0
        "http://0.0.0.0:10008",  # GPU 2
    ]
    
    generator_2gpu = Generator(
        endpoint=two_gpu_endpoints,
        seed=42,
        output_folder=Path("./output_2gpu"),
        echo=print
    )
    
    print()
    
    # ========================================================================
    # EXAMPLE 5: Remote Servers
    # ========================================================================
    print("=" * 70)
    print("Example 5: Using Remote Servers")
    print("=" * 70)
    
    remote_endpoints = [
        "http://192.168.1.100:10006",
        "http://192.168.1.101:10006",
        "http://192.168.1.102:10006",
        "http://192.168.1.103:10006",
    ]
    
    generator_remote = Generator(
        endpoint=remote_endpoints,
        seed=42,
        output_folder=Path("./output_remote"),
        echo=print
    )
    
    print()
    
    print("=" * 70)
    print("Examples Complete!")
    print("=" * 70)
    print()
    print("Key Benefits of Multi-Port Setup:")
    print("  ✓ 4x throughput (4.8 requests/min vs 1.2 requests/min)")
    print("  ✓ Automatic load balancing (round-robin)")
    print("  ✓ Better GPU utilization")
    print("  ✓ Same latency per request (~45-50s)")
    print()
    print("Usage:")
    print("  1. Start servers: cd /root/3d-genius && ./start_multi_port.sh")
    print("  2. Update endpoint list in your code")
    print("  3. Run your generation script")
    print()


if __name__ == "__main__":
    asyncio.run(main())

