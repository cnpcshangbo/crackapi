# Usages:
```
cd PointCloud2BinaryImage
python3 CrackAnalyzer.py
```
## Case 0:
http://127.0.0.1:5002/analyze_crack?click1_x=0.08817603&click1_y=0.10874449&click2_x=0.11819754&click2_y=0.14

{
  "total_crack_length": 0
}

## Case 1:
http://127.0.0.1:5002/analyze_crack?click1_x=-10&click1_y=11&click2_x=0&click2_y=20

{
  "total_crack_length": 261.0
}