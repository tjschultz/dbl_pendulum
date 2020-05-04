# Double pendulum animation by Tyler J. Schultz for MAP2302.0H1 project
import tkinter as tk
import random
import math as m

# constants
G = 9.81 # m/s^2
N_COMP_PENDULUMS = 2 # set number of double pendulums to animate


"""class describing a single pendulum"""
class Pendulum:
    
    def __init__(self, theta: float, thetadot: float,
                 mass: float, length: float,
                 width: int = 2):
        self.theta = theta
        self.thetadot = thetadot
        self.mass = mass
        self.length = length
        self.width = width

"""app that will house the canvas for animating the pendulum. In this case, each double pendulum
is composed of a pendulum at the same index in two parallel array structures,
pendulum1 and pendulum2 i.e. the ith double pendulum is
made of parts pendulums1[i] and pendulums2[i]"""
class App(tk.Tk):

    pendulums1 = []
    pendulums2 = []
    
    def __init__(self,
                 pendulums1: [], pendulums2: [],
                 width: int = 600,
                 height: int = 600,offset_width: int = 300,
                 offset_height: int = 120,
                 dt: float = 0.05):
        # set attributes
        self.width = width
        self.height = height
        self.offset_width = offset_width
        self.offset_height = offset_height
        self.dt = dt

        # set pendulums
        self.pendulums1 = pendulums1
        self.pendulums2 = pendulums2
        self.trace_coords = []

        # setting canvas widget
        tk.Tk.__init__(self)
        self.title("Double Rod Pendulum")
        self.canvas = tk.Canvas(self,
                                width=self.width, height=self.height)
        self.canvas.pack(side="top")

        # action
        self.after(1, self.draw_frame)


    """method that updates the object variables of each pendulum"""
    def update_pendulum_pos(self, index):

        # create dummy pendulum objects
        p1 = self.pendulums1[index]
        p2 = self.pendulums2[index]
        
        # create forms for the numerators and denominators of the equations of motion
        # A, B, C, Q, R, S, T, den1, den2

        # pendulum1
        
        A = -G * (2 * p1.mass + p2.mass) # -g(2*(m1+m2))
        A *= m.sin(p1.theta) # *sin(theta1)

        B = -p2.mass * G # -m2*G
        B *= m.sin(     # sin(theta1-2*theta2)
            p1.theta -
            2 * p2.theta)

        C = -2 * m.sin(p1.theta-p2.theta) # -2*sin(theta1-theta2)
        C *= p2.mass                      # * m2
        C *= (                                  # *(theta2dot^2 * L2 + theta1dot^2 * L1)*cos(theta1-theta2)
            p2.thetadot**2 * p2.length +
            p1.thetadot**2 * p1.length *
            m.cos(
                p1.theta -
                p2.theta
            )
        )

        den1 = p1.length * (    # DEN1 = L1(2*m1 + m2*cos(2*theta1-2*theta2)
            2 * p1.mass +
            p2.mass -
            p2.mass *
            m.cos(
                2 * p1.theta -
                2 * p2.theta
            )
        )

        # pendulum2
        
        Q = 2 * m.sin(p1.theta - p2.theta)  # 2sin(theta1-theta2)

        R = (                               # (theta1dot^2*L1*(m1+m2))
            p1.thetadot**2 *
            p1.length *
            (p1.mass + p2.mass)
        )

        S = G * (p1.mass + p2.mass)         # G(m1 + m2)
        S *= m.cos(p1.theta)                # *cos(theta1)

        T = p2.thetadot**2 * p2.length      # theta2dot^2 * L2
        T *= p2.mass * m.cos(               # *(m2*cos(theta1-theta2))
            p1.theta -
            p2.theta
        )

        den2 = p2.length * (    # DEN2 = L2(2*m1 + m2*cos(2*theta1-2*theta2)
            2 * p1.mass +
            p2.mass -
            p2.mass *
            m.cos(
                2 * p1.theta -
                2 * p2.theta
            )
        )

        # use the computed quantities to find the second derivatives (acc) of each pendulum
        theta1dotdot = (A + B + C) / den1
        theta2dotdot = (Q*(R+S+T)) / den2

        # update the corresponding pendulums in the original array passed to the App class
        self.pendulums1[index].thetadot += theta1dotdot * self.dt
        self.pendulums1[index].theta +=  p1.thetadot * self.dt
        self.pendulums2[index].thetadot += theta2dotdot * self.dt
        self.pendulums2[index].theta +=  p2.thetadot * self.dt


    """draws the pendulums and a trace"""
    def draw_pendulums(self, index):

        # create dummy pendulum objects
        p1 = self.pendulums1[index]
        p2 = self.pendulums2[index]

        # cartesian conversion 
        x1 = p1.length * m.sin(p1.theta)
        y1 = p1.length * m.cos(p1.theta)

        x2 = x1 + p2.length * m.sin(p2.theta)
        y2 = y1 + p2.length * m.cos(p2.theta)

        # append the resultant trace from the coords
        self.trace_coords.append(
            (
                self.offset_width + x2,
                self.offset_height + y2,
                self.offset_width + x2,
                self.offset_height + y2
            )
        )

        # draw the trace
        self.canvas.create_line(self.trace_coords, fill='blue', tag='trace')

        # Draw the first pendulum
        self.canvas.create_line(
            self.offset_width, self.offset_height,
            self.offset_width + x1, self.offset_height + y1,
            width=p1.width, fill='orange', tags='pendulum'
        )
        

        # Draw the second pendulum
        self.canvas.create_line(
            self.offset_width + x1, self.offset_height + y1,
            self.offset_width + x2, self.offset_height + y2,
            width=p2.width, fill='orange', tags='pendulum'
        )

    """draw the current frame"""
    def draw_frame(self):

        # Delete objects on the canvas to redraw
        self.canvas.delete('trace')
        self.canvas.delete('pendulum')

        # Update the positions and draw the frame
        for i in range(N_COMP_PENDULUMS):
            self.update_pendulum_pos(i)
            self.draw_pendulums(i)

        # Repeat
        self.after(1, self.draw_frame)

# main method
if __name__ == '__main__':
        
    pendulums_1 = []

    pendulums_2 = []


    for i in range(N_COMP_PENDULUMS):
        # Initialization of the two pendulums
        theta1 = random.random() * 2 * m.pi
        theta2 = random.random() * 2 * m.pi

        pendulum_1_parameters = {
            "theta": theta1,
            "thetadot": 0,
            "mass": 10,
            "length": 100,
            "width": 3
        }

        pendulum_2_parameters = {
            "theta": theta2,
            "thetadot": 0,
            "mass": 10,
            "length": 100,
            "width": 3
        }
            
        pendulum_1 = Pendulum(**pendulum_1_parameters)
        pendulums_1.append(pendulum_1)

        pendulum_2 = Pendulum(**pendulum_2_parameters)
        pendulums_2.append(pendulum_2)

    # Run the animation
    animation_parameters = {
        "pendulums1": pendulums_1,
        "pendulums2": pendulums_2,
        "width": 600,
        "height": 600,
        "offset_width": 300,
        "offset_height": 150,
        "dt": 0.1
    }
    app = App(**animation_parameters)
    app.mainloop()

        
