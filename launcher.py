#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OmniVoice AMD GPU Edition - Launcher"""

import os
import sys
import subprocess
import socket
import string
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def find_model_cache():
    """Auto-detect model cache directory"""
    # Priority 1: Current directory
    current_models = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
    
    # Priority 2: Scan all mounted drives (more efficient)
    drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
    logger.debug(f"Available drives: {drives}")
    
    possible_paths = [current_models]
    
    for drive in drives:
        possible_paths.extend([
            f"{drive}OmniVoice_amd-gpu-master\\models",
            f"{drive}OmniVoice\\models",
            f"{drive}OmniVoice\\release\\models",
        ])
    
    # Check each path for existing models
    for path in possible_paths:
        hub_path = os.path.join(path, "hub")
        try:
            if os.path.exists(hub_path):
                models = os.listdir(hub_path)
                if any("OmniVoice" in m or "k2-fsa" in m for m in models):
                    logger.info(f"Found model cache at: {path}")
                    return path
        except (FileNotFoundError, PermissionError) as e:
            logger.debug(f"Cannot access {hub_path}: {e}")
            continue
    
    # No existing models found, use current directory
    # Create models folder if not exists
    if not os.path.exists(current_models):
        os.makedirs(current_models, exist_ok=True)
        logger.info(f"Created model cache directory: {current_models}")
    
    return current_models

def check_port(host, port, timeout=1):
    """Check if a port is open"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        return result == 0
    except Exception as e:
        logger.debug(f"Error checking port {port}: {e}")
        return False
    finally:
        sock.close()

def detect_proxy():
    """Auto-detect common proxy ports"""
    common_ports = [
        (7890, "Clash/V2Ray"),
        (1080, "SOCKS5"),
        (8080, "HTTP Proxy"),
        (10809, "V2RayN"),
    ]
    
    for port, name in common_ports:
        if check_port("127.0.0.1", port):
            logger.info(f"Detected proxy: {name} on port {port}")
            return f"http://127.0.0.1:{port}", name
    return None, None

def setup_env():
    """Setup environment variables with auto-detection"""
    # Find model cache
    model_cache = find_model_cache()
    
    # Always use mirror
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
    os.environ["HF_HOME"] = model_cache
    os.environ["MIOPEN_LOG_LEVEL"] = "6"
    
    logger.debug(f"HF_ENDPOINT: {os.environ['HF_ENDPOINT']}")
    logger.debug(f"HF_HOME: {os.environ['HF_HOME']}")
    
    # Auto-detect proxy
    proxy_url, proxy_name = detect_proxy()
    
    if proxy_url:
        os.environ["HTTP_PROXY"] = proxy_url
        os.environ["HTTPS_PROXY"] = proxy_url
        logger.debug(f"Proxy set: {proxy_url} ({proxy_name})")
        return model_cache, proxy_url, proxy_name
    
    logger.debug("No proxy detected")
    return model_cache, None, None

def main():
    # Setup environment with auto-detection
    model_cache, proxy_url, proxy_name = setup_env()
    
    print(f"[Config] Model cache: {model_cache}")
    print(f"[Config] HF mirror: https://hf-mirror.com")
    
    if proxy_url:
        print(f"[Config] Proxy: {proxy_url} ({proxy_name})")
    else:
        print("[Config] Proxy: none")
    
    print()
    print("=" * 60)
    print("     OmniVoice AMD GPU Edition")
    print("=" * 60)
    print()
    print("请选择:")
    print("   1. 启动 Web 界面 (推荐)")
    print("   2. 验证安装")
    print("   3. 退出")
    print()
    
    try:
        choice = input("请输入选项 (1/2/3): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\n中断")
        sys.exit(0)
    
    print()
    
    if choice == "1":
        print("正在启动 Web 界面...")
        print()
        print("请在浏览器中打开: http://localhost:8001")
        print()
        print("按 Ctrl+C 停止服务")
        print()
        try:
            from omnivoice.cli.demo import main as demo_main
            sys.argv = ["omnivoice-demo", "--ip", "0.0.0.0", "--port", "8001"]
            demo_main()
        except KeyboardInterrupt:
            print("\n服务已停止")
        except Exception as e:
            logger.error(f"Failed to start web UI: {e}")
            print(f"启动失败: {e}")
            
    elif choice == "2":
        verify_script = os.path.join(os.path.dirname(__file__), "verify_install.py")
        subprocess.run([sys.executable, verify_script])
        
    elif choice == "3":
        print("再见!")
        return
    else:
        print("无效选项")

if __name__ == "__main__":
    main()
