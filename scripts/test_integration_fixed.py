#!/usr/bin/env python3
"""Fixed Test Integration Between Agents and Tools
Tests if agents can properly use tools and communicate with each other
"""

import os
import json
import sys
from pathlib import Path

def test_agent_orchestrator():
    """Test Agent Orchestrator functionality."""
    try:
        from agents.agent_orchestrator import AgentOrchestrator
        print("🧪 Testing Agent Orchestrator...")
        
        orchestrator = AgentOrchestrator()
        status = orchestrator.get_status()
        print(f"✅ Agent Orchestrator status: {status}")
        
        # Test agent registration
        test_agents = ["audio_processor", "video_editor", "social_media", "content_distributor"]
        
        for agent_name in test_agents:
            class MockAgent:
                def __init__(self):
                    self.name = agent_name
                    self.capabilities = ["test_capability_1", "test_capability_2"]
                    self.status = "ready"
                
                def get_capabilities(self):
                    return self.capabilities
        
            agent_instance = MockAgent(agent_name)
            success = orchestrator.register_agent(agent_name, agent_instance, agent_instance.get_capabilities())
            if success:
                print(f"✅ Agent {agent_name} registered successfully")
            else:
                print(f"❌ Agent {agent_name} registration failed")
        
        registered_count = sum(1 for success in [orchestrator.get_all_agents()])
        print(f"📋 Agent Registration Test: {registered_count}/{len(test_agents)} agents passed")
    
    except Exception as e:
        print(f"❌ Agent Orchestrator test failed: {e}")
        return False

def test_tool_communication():
    """Test if agents can communicate with tools"""
    print("🔧 Testing Tool Communication...")
    
    try:
        from agents.production_agent import ProductionAgent
        production_agent = ProductionAgent()
        social_media_agent = SocialMediaAgent()
        
        # Test tool access
        production_tools = production_agent.get_tools()
        social_media_tools = social_media_agent.get_tools()
        
        print(f"✅ Production tools available: {list(production_tools.keys())}")
        print(f"✅ Social Media tools available: {list(social_media_tools.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Tool Communication test failed: {e}")
        return False

def test_integration():
    """Run all integration tests"""
    print("🚀 Starting Integration Tests")
    
    success_count = 0
    total_tests = 6
    
    # Run tests
    test_results = [
        test_agent_orchestrator(),
        test_tool_communication(),
        SimpleAudioProcessor().process_audio_pipeline(
            input_file="test_data/sample.wav",
            output_dir="/tmp/integration_test"
            noise_reduction=True,
            voice_enhancement=True,
            compression=True,
            normalization=True
        )
    ]
    
    for i, result in enumerate(test_results, 1):
        print(f"🔄 Test {i+1}/{total_tests}: {result['success']}")
    
    passed = sum(1 for r in test_results if r["success"])
    
    print("\n" + "="*50)
    print("📊 INTEGRATION TEST SUMMARY")
    print("="*50)
    print(f"📊 Tests Passed: {passed}/{total_tests}")
    
    if passed == total_tests:
        print("🎉 All tests passed! System is ready for automation.")
        return 0
    else:
        print("⚠️  Some tests failed. System needs attention.")
        return 1

if __name__ == "__main__":
    exit(test_integration())