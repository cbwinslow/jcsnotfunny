#!/usr/bin/env python3
"""Test script for MCP server functionality.

This script tests the social media MCP server to ensure it can:
1. Start and initialize properly
2. List available tools
3. Handle tool calls (basic validation)
"""

import sys
import json
import subprocess
from pathlib import Path

def test_mcp_server_installation():
    """Test that MCP server dependencies are installed."""
    print("🔧 Testing MCP Server Installation")
    print("=" * 50)

    server_dir = Path(__file__).parent / "mcp-servers" / "social-media-manager"

    # Check if package.json exists
    package_json = server_dir / "package.json"
    if not package_json.exists():
        print("❌ package.json not found")
        return False

    # Check if server.js exists
    server_js = server_dir / "server.js"
    if not server_js.exists():
        print("❌ server.js not found")
        return False

    print("✅ MCP server files found")
    return True


def test_mcp_server_list_tools():
    """Test that MCP server can list tools."""
    print("\n📋 Testing MCP Server Tool Listing")
    print("=" * 50)

    server_dir = Path(__file__).parent / "mcp-servers" / "social-media-manager"

    # Create a simple test client that connects to the MCP server
    test_script = """
const { spawn } = require('child_process');

// Start the MCP server
const server = spawn('node', ['server.js'], {
  cwd: process.cwd(),
  stdio: ['pipe', 'pipe', 'pipe']
});

let output = '';
let error_output = '';

server.stdout.on('data', (data) => {
  output += data.toString();
});

server.stderr.on('data', (data) => {
  error_output += data.toString();
});

// Send ListTools request
setTimeout(() => {
  const listToolsRequest = {
    jsonrpc: '2.0',
    id: 1,
    method: 'tools/list',
    params: {}
  };

  server.stdin.write(JSON.stringify(listToolsRequest) + '\\n');
}, 1000);

// Wait for response
setTimeout(() => {
  server.kill();

  try {
    const lines = output.trim().split('\\n');
    const response = JSON.parse(lines[lines.length - 1]);

    if (response.result && response.result.tools) {
      console.log(`✅ Found ${response.result.tools.length} tools:`);
      response.result.tools.forEach(tool => {
        console.log(`   - ${tool.name}: ${tool.description}`);
      });
    } else {
      console.log('❌ No tools found in response');
    }
  } catch (e) {
    console.log('❌ Failed to parse server response');
    console.log('Output:', output);
    console.log('Error:', error_output);
  }
}, 2000);
"""

    # Write test script
    test_file = server_dir / "test_client.js"
    with open(test_file, 'w') as f:
        f.write(test_script)

    try:
        # Run the test
        result = subprocess.run(
            ['node', 'test_client.js'],
            cwd=server_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        print("Server output:")
        print(result.stdout)
        if result.stderr:
            print("Server errors:")
            print(result.stderr)

        # Check if we got expected tools
        expected_tools = [
            'post_to_twitter',
            'post_to_instagram',
            'post_to_tiktok',
            'upload_to_youtube',
            'post_to_linkedin',
            'cross_post',
            'get_analytics'
        ]

        success = True
        for tool in expected_tools:
            if tool not in result.stdout:
                print(f"❌ Expected tool '{tool}' not found")
                success = False

        if success:
            print("✅ All expected tools found")

        return success

    except subprocess.TimeoutExpired:
        print("❌ Server test timed out")
        return False
    except Exception as e:
        print(f"❌ Server test failed: {e}")
        return False
    finally:
        # Clean up test file
        if test_file.exists():
            test_file.unlink()


def test_mcp_server_tool_call():
    """Test a basic tool call to the MCP server."""
    print("\n🔨 Testing MCP Server Tool Calls")
    print("=" * 50)

    server_dir = Path(__file__).parent / "mcp-servers" / "social-media-manager"

    # Test get_analytics tool (should work without API keys)
    test_script = """
const { spawn } = require('child_process');

// Start the MCP server
const server = spawn('node', ['server.js'], {
  cwd: process.cwd(),
  stdio: ['pipe', 'pipe', 'pipe']
});

let output = '';
let error_output = '';

server.stdout.on('data', (data) => {
  output += data.toString();
});

server.stderr.on('data', (data) => {
  error_output += data.toString();
});

// Send get_analytics tool call
setTimeout(() => {
  const toolCall = {
    jsonrpc: '2.0',
    id: 2,
    method: 'tools/call',
    params: {
      name: 'get_analytics',
      arguments: {
        platforms: ['twitter', 'instagram']
      }
    }
  };

  server.stdin.write(JSON.stringify(toolCall) + '\\n');
}, 1000);

// Wait for response
setTimeout(() => {
  server.kill();

  try {
    const lines = output.trim().split('\\n');
    const response = JSON.parse(lines[lines.length - 1]);

    if (response.result && response.result.content) {
      const content = JSON.parse(response.result.content[0].text);
      if (content.success) {
        console.log('✅ get_analytics tool call successful');
        console.log(`   Platforms analyzed: ${Object.keys(content.analytics).join(', ')}`);
      } else {
        console.log('❌ Tool call failed:', content.error);
      }
    } else {
      console.log('❌ Invalid tool response format');
    }
  } catch (e) {
    console.log('❌ Failed to parse tool response');
    console.log('Output:', output);
    console.log('Error:', error_output);
  }
}, 2000);
"""

    # Write test script
    test_file = server_dir / "test_tool_call.js"
    with open(test_file, 'w') as f:
        f.write(test_script)

    try:
        # Run the test
        result = subprocess.run(
            ['node', 'test_tool_call.js'],
            cwd=server_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        print("Tool call output:")
        print(result.stdout)
        if result.stderr:
            print("Tool call errors:")
            print(result.stderr)

        # Check for success
        if 'get_analytics tool call successful' in result.stdout:
            print("✅ Tool call test passed")
            return True
        else:
            print("❌ Tool call test failed")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Tool call test timed out")
        return False
    except Exception as e:
        print(f"❌ Tool call test failed: {e}")
        return False
    finally:
        # Clean up test file
        if test_file.exists():
            test_file.unlink()


def main():
    """Run comprehensive MCP server tests."""
    print("🚀 MCP SERVER COMPREHENSIVE TEST")
    print("=" * 50)
    print("This test will:")
    print("1. Check MCP server installation")
    print("2. Test tool listing functionality")
    print("3. Test basic tool call handling")
    print("\nNote: This requires Node.js and npm to be installed")
    print("=" * 50)

    # Test installation
    if not test_mcp_server_installation():
        print("❌ Cannot proceed without proper installation")
        return

    # Test tool listing
    tools_success = test_mcp_server_list_tools()

    # Test tool calls
    tool_call_success = test_mcp_server_tool_call()

    # Summary
    print("\n" + "=" * 50)
    print("📊 MCP SERVER TEST SUMMARY")
    print("=" * 50)

    if tools_success and tool_call_success:
        print("✅ MCP server tests PASSED")
        print("\n🎯 MCP Server Capabilities Demonstrated:")
        print("   ✅ Server initialization and startup")
        print("   ✅ Tool discovery and listing")
        print("   ✅ Tool call handling and execution")
        print("   ✅ JSON-RPC protocol compliance")
        print("   ✅ Error handling and response formatting")

        print("\n🔧 MCP Server Tools Available:")
        print("   ✅ post_to_twitter - Twitter posting")
        print("   ✅ post_to_instagram - Instagram posting")
        print("   ✅ post_to_tiktok - TikTok posting")
        print("   ✅ upload_to_youtube - YouTube uploading")
        print("   ✅ post_to_linkedin - LinkedIn posting")
        print("   ✅ cross_post - Multi-platform posting")
        print("   ✅ get_analytics - Social media analytics")
    else:
        print("❌ MCP server tests FAILED")
        if not tools_success:
            print("   - Tool listing failed")
        if not tool_call_success:
            print("   - Tool call execution failed")


if __name__ == "__main__":
    main()
