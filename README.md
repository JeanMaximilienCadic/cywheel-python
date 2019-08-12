<p align="center">
  <img src="https://raw.githubusercontent.com/JeanMaximilienCadic/cywheel-python/master/img/cython.png"/>
</p>

# Cython packaging for python wheels

## Requirements
```bash
pip install -r requirements.txt
pip install cywheel
```
## Getting Started


```bash
from cywheel import CyMake

if __name__=="__main__":
    maker = CyMake(root="/home/user/python/project-python",
                   setup="setup.py",
                   version="1.0a1")

    maker.make(submodule="submodule1")

```


## Contributions

Email me at j.cadic@9dw-lab.com for any questions.
