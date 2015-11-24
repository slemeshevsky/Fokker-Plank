#!/bin/bash -x
./plotting.py ./Results_17_09/Bi-Si_1MeV_dx=1_N=4001 --xrange 800 4500 --logscale --ymin 1e-6
./plotting.py ./Results_17_09/Bi-Si_1MeV_dx=1_N=4001_Nmju=101 --xrange 800 4500 --logscale --ymin 1e-6
./plotting.py ./Results_17_09/Bi-Si_50MeV_dx=100_N=16001 --xrange 50000 105000 --logscale --ymin 1e-9
./plotting.py ./Results_17_09/Bi-Si_50MeV_dx=100_N=50001_Nmju=101 --xrange 50000 105000 --logscale --ymin 1e-9
./plotting.py ./Results_17_09/B-Si_1MeV_dx=1_N=2001 --xrange 9000 25000 --logscale --ymin 1e-8
./plotting.py ./Results_17_09/B-Si_1MeV_dx=1_N=2001_Nmju=101 --xrange 9000 25000 --logscale --ymin 1e-8
./plotting.py ./Results_17_09/B-Si_50MeV_dx=1_N=8001_Nmju=101 --xrange 8e5 940000 --logscale --ymin 1e-9
./plotting.py ./Results_17_09/P-Si_1MeV_dx=1_N=2001 --xrange 4000 17000 --logscale --ymin 1e-8
./plotting.py ./Results_17_09/P-Si_50MeV_dx=1_N=10001_Nmju=101 --xrange 150000 185000 --logscale --ymin 1e-8
./plotting.py ./Results_17_09/P-Si_50MeV_dx=1_N=20001 --xrange 150000 185000 --logscale --ymin 1e-8

