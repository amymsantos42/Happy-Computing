
from utils import *
from entidades import *

if __name__ == '__main__':
    print('='*70)
    print('Comezando la Simulacion')
    w = Tienda()
    y = [w.simular() for i in range(1000)]

    print(f'La ganancia media es de {sum(y)/1000}')
    print(f'La ganancia minima es de {min(y)}')
    print(f'La ganancia maxima es de {max(y)}')
    
    print('Fin')