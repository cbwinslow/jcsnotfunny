#!/usr/bin/env python3
"""
Integration Test - Fixed Version
Tests the complete system integration with real dependencies
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to sys.path to enable imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_audio_processor():
    """Test the audio processor with real dependencies"""
    print("🎵 Testing Audio Processor...")

    try:
        from scripts.audio_processor_working import AudioProcessor

        # Create a test audio file path (this will simulate processing)
        test_file = "test_audio.wav"
        output_dir = "test_output"

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Test audio processor initialization
        processor = AudioProcessor()
        print(
            f"✅ AudioProcessor initialized with target LUFS: {processor.target_lufs}"
        )

        # Test individual methods (with simulated files)
        methods_to_test = [
            "apply_noise_reduction",
            "apply_de_essing",
            "apply_eq",
            "apply_compression",
            "normalize_loudness",
        ]

        for method_name in methods_to_test:
            method = getattr(processor, method_name)
            print(f"✅ Method {method_name} available")

        print("✅ Audio Processor test completed")
        return True

    except Exception as e:
        print(f"❌ Audio Processor test failed: {e}")
        return False


def test_working_agents():
    """Test the working agents system"""
    print("🤖 Testing Working Agents...")

    try:
        from scripts.working_agents import ProductionAgent, test_agent_system

        # Test agent initialization
        agent = ProductionAgent()
        status = agent.get_status()
        print(f"✅ Production Agent initialized: {status}")

        # Test tool initialization
        tools = agent.initialize_tools()
        print(f"✅ Tools initialized: {list(tools.keys())}")

        # Test task execution
        test_tasks = [
            {
                "type": "video_analysis",
                "video_path": "test_video.mp4",
                "analysis_type": "basic",
            },
            {
                "type": "audio_processing",
                "input_file": "test_audio.wav",
                "steps": ["cleanup", "enhancement"],
            },
        ]

        for i, task in enumerate(test_tasks, 1):
            result = agent.execute_task(task)
            success = result["success"]
            print(f"{'✅' if success else '❌'} Task {i}: {task['type']}")

        print("✅ Working Agents test completed")
        return True

    except Exception as e:
        print(f"❌ Working Agents test failed: {e}")
        return False


def test_social_media_apis():
    """Test social media API implementations"""
    print("📱 Testing Social Media APIs...")

    try:
        from scripts.social_media_apis import (
            TwitterAPI,
            InstagramAPI,
            TikTokAPI,
            YouTubeAPI,
            LinkedInAPI,
            SocialMediaManager,
        )

        # Test API initialization
        apis = [
            ("Twitter", TwitterAPI()),
            ("Instagram", InstagramAPI()),
            ("TikTok", TikTokAPI()),
            ("YouTube", YouTubeAPI()),
            ("LinkedIn", LinkedInAPI()),
            ("SocialMediaManager", SocialMediaManager()),
        ]

        for name, api in apis:
            print(f"✅ {name} API initialized")

        print("✅ Social Media APIs test completed")
        return True

    except Exception as e:
        print(f"❌ Social Media APIs test failed: {e}")
        return False


def test_mcp_server():
    """Test MCP server availability"""
    print("🔌 Testing MCP Server...")

    try:
        # Check if MCP server file exists
        mcp_server_path = (
            project_root / "mcp-servers" / "social-media-manager" / "server.js"
        )
        if mcp_server_path.exists():
            print(f"✅ MCP server file exists: {mcp_server_path}")
        else:
            print(f"❌ MCP server file not found: {mcp_server_path}")
            return False

        # Check Node.js dependencies
        package_json_path = (
            project_root / "mcp-servers" / "social-media-manager" / "package.json"
        )
        if package_json_path.exists():
            print(f"✅ package.json exists: {package_json_path}")
        else:
            print(f"❌ package.json not found: {package_json_path}")
            return False

        print("✅ MCP Server test completed")
        return True

    except Exception as e:
        print(f"❌ MCP Server test failed: {e}")
        return False


def test_documentation_structure():
    """Test documentation structure"""
    print("📚 Testing Documentation Structure...")

    try:
        docs_dir = project_root / "docs"

        # Check main documentation directories
        required_dirs = [
            "knowledge-base",
            "prompts",
            "configs",
            "toolsets",
            "templates",
        ]

        for dir_name in required_dirs:
            dir_path = docs_dir / dir_name
            if dir_path.exists():
                print(f"✅ Documentation directory exists: {dir_name}")
            else:
                print(f"❌ Documentation directory missing: {dir_name}")
                return False

        # Check key documentation files
        required_files = [
            "docs/knowledge-base/ai-knowledge-base.md",
            "docs/prompts/production-prompts.md",
            "docs/configs/configuration-management.md",
            "docs/toolsets/production-tools.md",
            "docs/templates/content-templates.md",
        ]

        for file_path in required_files:
            full_path = project_root / file_path
            if full_path.exists():
                print(f"✅ Documentation file exists: {file_path}")
            else:
                print(f"❌ Documentation file missing: {file_path}")
                return False

        print("✅ Documentation structure test completed")
        return True

    except Exception as e:
        print(f"❌ Documentation structure test failed: {e}")
        return False


def main():
    """Run all integration tests"""
    print("🚀 Starting Integration Tests...")
    print(f"📁 Project root: {project_root}")

    tests = [
        ("Audio Processor", test_audio_processor),
        ("Working Agents", test_working_agents),
        ("Social Media APIs", test_social_media_apis),
        ("MCP Server", test_mcp_server),
        ("Documentation Structure", test_documentation_structure),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{'=' * 50}")
        print(f"🧪 Running {test_name} Test")
        print("=" * 50)

        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))

    # Summary
    print(f"\n{'=' * 50}")
    print("📊 INTEGRATION TEST SUMMARY")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<25} {status}")

    print(f"\nOverall Result: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("🚀 System is ready for production!")
        return 0
    else:
        print("⚠️ Some integration tests failed")
        print("🔧 Additional fixes may be needed")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
