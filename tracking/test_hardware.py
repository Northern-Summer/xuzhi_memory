#!/usr/bin/env python3
"""Hardware Capability Test | Γ"""
import sys
import torch
import psutil

print("="*50)
print("Hardware Capability Test | Γ")
print("="*50)

# CPU
print(f"\nCPU: {psutil.cpu_count()} cores")

# RAM
ram = psutil.virtual_memory()
print(f"RAM: {ram.total / (1024**3):.1f} GB ({ram.available / (1024**3):.1f} GB available)")

# GPU
if torch.cuda.is_available():
    gpu_name = torch.cuda.get_device_name(0)
    gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    print(f"GPU: {gpu_name} ({gpu_mem:.1f} GB)")
    
    # Test small tensor
    try:
        x = torch.randn(1000, 1000, device='cuda')
        print(f"✓ CUDA tensor test passed")
        del x
        torch.cuda.empty_cache()
    except Exception as e:
        print(f"✗ CUDA test failed: {e}")
else:
    print("✗ CUDA not available")

# RDKit test
try:
    from rdkit import Chem
    from rdkit.Chem import AllChem
    mol = Chem.MolFromSmiles('CC(=O)Oc1ccccc1C(=O)O')  # Aspirin
    AllChem.Compute2DCoords(mol)
    print(f"✓ RDKit test passed")
except ImportError:
    print("✗ RDKit not installed")
except Exception as e:
    print(f"✗ RDKit test failed: {e}")

print("\n" + "="*50)
print("Recommendation based on this hardware:")
if ram.total < 8 * (1024**3):
    print("- RAM severely limited (< 8GB)")
    print("- Focus: ChemistryAI4S (lightweight)")
    print("- Avoid: AlphaFold 3, large-scale DFT")
print("="*50)
