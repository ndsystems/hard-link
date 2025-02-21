"""MMCore hardware abstraction layer access as RPC"""
import time
import os
from typing import Optional
from contextlib import contextmanager
from configs import config
import pymmcore
import rpyc
from comms import server
from collections import OrderedDict

mm_dir = config["mm_dir"]
config_path = config["mm_config"]
working_dir = os.getcwd()

class MMCoreError(Exception):
    """Custom exception for MMCore-related errors"""
    pass

@contextmanager
def mm_directory():
    """Context manager to handle directory changes safely"""
    original_dir = os.getcwd()
    try:
        os.chdir(mm_dir)
        yield
    finally:
        os.chdir(original_dir)

def create_mmc_obj() -> pymmcore.CMMCore:
    """
    Create and initialize MMCore object with proper error handling
    
    Returns:
        pymmcore.CMMCore: Initialized MMCore instance
    
    Raises:
        MMCoreError: If initialization or configuration loading fails
    """
    try:
        print("Creating MMCore instance...")
        mmc = pymmcore.CMMCore()
        mmc.setDeviceAdapterSearchPaths([mm_dir])
        mmc.loadSystemConfiguration(config_path)
        return mmc
    except Exception as e:
        raise MMCoreError(f"Failed to initialize MMCore: {str(e)}")

def unload(mmc: Optional[pymmcore.CMMCore] = None) -> None:
    """Safely unload and reset MMCore"""
    if mmc is not None:
        try:
            print("Unloading MMCore...")
            mmc.reset()
        except Exception as e:
            print(f"Error during MMCore unload: {str(e)}")

# Initialize MMCore in the correct directory
with mm_directory():
    mmc = create_mmc_obj()

class Microscope(rpyc.Service):
    """RPC Service for microscope control"""
    
    def __init__(self):
        super().__init__()
        self.mmc: Optional[pymmcore.CMMCore] = None

    def on_connect(self, conn):
        """Handle client connection and initialize MMCore reference"""
        print("Client connected")
        self.mmc = mmc

    def on_disconnect(self, conn):
        """Handle client disconnection"""
        print("Client disconnected")
        self.mmc = None

if __name__ == "__main__":
    try:
        s = server(Microscope, **config["mm_server"])
        s.start()
    finally:
        unload(mmc)