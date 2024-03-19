import numpy as np
from time import sleep
from random import random
import sympy as sp
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib.animation import FuncAnimation
from tqdm import tqdm
import itertools



#Draw double pendulum
class Pendulum():
    def __init__(self, l1, l2, m1, m2, theta1_0, theta2_0, v1_0, v2_0):
        self.m1 = m1
        self.l1 = l1
        self.m2 = m2
        self.l2 = l2
        self.conds = [theta1_0, v1_0, theta2_0, v2_0]
    
    def realtime(self, fps, tres=0.03):
        acc1, acc2 = self.solve_pendulum()
        l = self.l1+self.l2
        fig = plt.figure()
        ax = plt.axes(xlim=(-l, l), ylim=(-l, l))
        ax.set_aspect('equal')
        ax.tick_params(left = False, right = False , labelleft = False , 
                labelbottom = False, bottom = False)
        ax.set_aspect('equal')
        self.theta1 = self.conds[0]
        self.dtheta1 = self.conds[1]
        self.theta2 = self.conds[2]
        self.dtheta2 = self.conds[3]
        ropes, = ax.plot([0, sp.sin(self.theta1)*self.l1, (sp.sin(self.theta1)*self.l1+sp.sin(self.theta2)*self.l2)], [0, -sp.cos(self.theta1)*self.l1, (-sp.cos(self.theta1)*self.l1-sp.cos(self.theta2)*self.l2)],'-', lw=3, color='black')
        pendulums, = ax.plot([sp.sin(self.theta1)*self.l1, (sp.sin(self.theta1)*self.l1+sp.sin(self.theta2)*self.l2)], [-sp.cos(self.theta1)*self.l1, (-sp.cos(self.theta1)*self.l1-sp.cos(self.theta2)*self.l2)], 'o', color='red')
        pen2x = [(sp.sin(self.theta1)*self.l1+sp.sin(self.theta2)*self.l2)]
        pen2y = [(-sp.cos(self.theta1)*self.l1-sp.cos(self.theta2)*self.l2)]
        history, = ax.plot(pen2x, pen2y, '--', lw=1.5, color='red', alpha=0.7)

        # animation function.  This is called sequentially
        def init():
            ropes.set_data([],[])
            pendulums.set_data([],[])
            history.set_data(pen2x, pen2y)
            return [ropes, pendulums, history]
        
        def update(i):
            
            self.theta1 += self.dtheta1*tres
            self.theta2 += self.dtheta2*tres
            self.dtheta1 += acc1(9.81, self.l1, self.l2, self.m1, self.m2, self.theta1, self.theta2, self.dtheta1, self.dtheta2).simplify()*tres
            self.dtheta2 += acc2(9.81, self.l1, self.l2, self.m1, self.m2, self.theta1, self.theta2, self.dtheta1, self.dtheta2).simplify()*tres
            pen2x.append((sp.sin(self.theta1)*self.l1+sp.sin(self.theta2)*self.l2))
            pen2y.append((-sp.cos(self.theta1)*self.l1-sp.cos(self.theta2)*self.l2))
            ropes.set_data([0, sp.sin(self.theta1)*self.l1, (sp.sin(self.theta1)*self.l1+sp.sin(self.theta2)*self.l2)], [0, -sp.cos(self.theta1)*self.l1, (-sp.cos(self.theta1)*self.l1-sp.cos(self.theta2)*self.l2)])
            pendulums.set_data([sp.sin(self.theta1)*self.l1, (sp.sin(self.theta1)*self.l1+sp.sin(self.theta2)*self.l2)], [-sp.cos(self.theta1)*self.l1, (-sp.cos(self.theta1)*self.l1-sp.cos(self.theta2)*self.l2)])
            history.set_data(pen2x, pen2y)
            return [ropes, pendulums, history]

        anim = FuncAnimation(
                               fig, 
                               update, 
                               init_func=init,
                               frames = None,
                               interval = 1000/fps, # in ms
                               )
        plt.show()


    def preanimate(self, frames, fps, tres=0.03):
        acc1, acc2 = self.solve_pendulum()
        posx = []
        posy = []
        self.theta1 = self.conds[0]
        self.dtheta1 = self.conds[1]
        self.theta2 = self.conds[2]
        self.dtheta2 = self.conds[3]
        l = self.l1+self.l2
        for i in tqdm(range(frames+1)):
            posx.append([0, sp.sin(self.theta1)*self.l1, (sp.sin(self.theta1)*self.l1+sp.sin(self.theta2)*self.l2)])
            posy.append([0, -sp.cos(self.theta1)*self.l1, (-sp.cos(self.theta1)*self.l1-sp.cos(self.theta2)*self.l2)])
            self.theta1 += self.dtheta1*tres
            self.theta2 += self.dtheta2*tres
            self.dtheta1 += acc1(9.81, self.l1, self.l2, self.m1, self.m2, self.theta1, self.theta2, self.dtheta1, self.dtheta2).simplify()*tres
            self.dtheta2 += acc2(9.81, self.l1, self.l2, self.m1, self.m2, self.theta1, self.theta2, self.dtheta1, self.dtheta2).simplify()*tres

        
        fig = plt.figure()
        ax = plt.axes(xlim=(-l, l), ylim=(-l, l))
        ax.set_aspect('equal')
        ax.tick_params(left = False, right = False , labelleft = False , 
                labelbottom = False, bottom = False)
        
        ropes, = ax.plot([0, sp.sin(self.theta1)*self.l1, (sp.sin(self.theta1)*self.l1+sp.sin(self.theta2)*self.l2)], [0, -sp.cos(self.theta1)*self.l1, (-sp.cos(self.theta1)*self.l1-sp.cos(self.theta2)*self.l2)],'-', color='black')
        pendulums, = ax.plot([sp.sin(self.theta1)*self.l1, (sp.sin(self.theta1)*self.l1+sp.sin(self.theta2)*self.l2)], [-sp.cos(self.theta1)*self.l1, (-sp.cos(self.theta1)*self.l1-sp.cos(self.theta2)*self.l2)], 'o', color='red')
        # animation function.  This is called sequentially
        def init():
            ropes.set_data([],[])
            pendulums.set_data([],[])
            return [ropes, pendulums]
        
        def update(i):
            
            ropes.set_data(posx[i], posy[i])
            pendulums.set_data(posx[i][1:], posy[i][1:])
            return [ropes, pendulums]

        anim = FuncAnimation(
                               fig, 
                               update, 
                               init_func=init,
                               frames = frames,
                               interval = 1000/fps, # in ms
                               )
        plt.show()

    def solve_pendulum(self):
        m1, m2, g, l1, l2, t = sp.symbols(('m1', 'm2', 'g', 'l1', 'l2', 't'))
        theta1 = sp.Function('theta1')(t)
        dtheta1 = theta1.diff(t)
        ddtheta1 = dtheta1.diff(t)
        theta2 = sp.Function('theta2')(t)
        dtheta2 = theta2.diff(t)
        ddtheta2 = dtheta2.diff(t)

        x1,y1 = l1*sp.sin(theta1), -l1*sp.cos(theta1)
        x2,y2 = l1*sp.sin(theta1)+l2*sp.sin(theta2), -l1*sp.cos(theta1)-l2*sp.cos(theta2)
        T = sp.Rational(1,2)*m1*(x1.diff(t)**2+y1.diff(t)**2)+sp.Rational(1,2)*m2*(x2.diff(t)**2+y2.diff(t)**2)
        V = m1*g*y1+m2*g*y2
        L = T-V

        #Euler-Lagrange
        lhs1 = L.diff(theta1)
        rhs1 = sp.diff(L.diff(dtheta1), t)

        eulerLagrange1 = rhs1-lhs1
        eulerLagrange1 = sp.solve(eulerLagrange1, ddtheta1)[0]

        acc1 = sp.lambdify((g,l1,l2,m1,m2,theta1,theta2,dtheta1,dtheta2), eulerLagrange1, modules=sp)

        lhs2 = L.diff(theta2)
        rhs2 = sp.diff(L.diff(dtheta2), t)

        eulerLagrange2 = rhs2-lhs2
        eulerLagrange2 = sp.solve(eulerLagrange2, ddtheta2)[0]
        print(eulerLagrange1, eulerLagrange2)
        acc2 = sp.lambdify((g,l1,l2,m1,m2,theta1,theta2,dtheta1,dtheta2), eulerLagrange2, modules=sp)
        return acc1, acc2



#initialize pendulum:
pendule = Pendulum(1, 1, 1, 1, random()*2*np.pi, random()*2*np.pi, random()*10-5, random()*10-5)
#pendule = Pendulum(2, 1, 1, 1, 2, 2, 0, 0)
#Animate:
pendule.realtime(60, tres=0.02)
#pendule.preanimate(1000, 30, 0.03)



