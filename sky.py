import pygame
import math
import cmath
import random

# [Moon]:
class Circles(): # All circles in the Apollo Gasket is a circle object, has: radius, (x,y) position, and a curvature

    def __init__(self, x, y, radius):
        self.r = radius
        self.pos = (x + y*1j) # Position of circle is stored as a real number and an imaginary number
                              # instead of a tuple or a list. X is defined as the real number, Y is
                              # defined as the imaginary number. 

    def curvature(self): # Circle's curvature is the reciprocal of its radius
        return 1/self.r
    
def outerTangCirc(circle1, circle2, circle3): # Function calculates a 4th tangent circle that encloses 3 tangent circles
    curv1 = circle1.curvature() 
    curv2 = circle2.curvature()
    curv3 = circle3.curvature()
    pos1 = circle1.pos
    pos2 = circle2.pos
    pos3 = circle3.pos
    
    # New position and curvature is calculated with Vieta's formula
    curv4 = -2 * cmath.sqrt(curv1*curv2 + curv2*curv3 + curv1*curv3) + curv1 + curv2 + curv3 
    pos4 = (-2 * cmath.sqrt(curv1*pos1*curv2*pos2 + curv2*pos2*curv3*pos3 + curv1*pos1*curv3*pos3 ) + curv1*pos1 + curv2*pos2 + curv3*pos3)/curv4
    circle4 = Circles(pos4.real, pos4.imag, 1/curv4) # New information is created into a Circles object
    return circle4

def innerTangCirc(circle2, circle3, circle4): # Function calculates an enclosed tangent circle, as well as a circle that encloses them
    r2 = circle2.r
    r3 = circle3.r
    r4 = circle4.r

    circle2 = Circles(0,0, r2)
    circle3 = Circles(r2 + r3, 0 , r3)
    x_of_4 = (r2*r2 + r2*r4 + r2*r3 - r3*r4)/(r2+r3)
    y_of_4 = cmath.sqrt((r2 + r4)*(r2 + r4) - x_of_4*x_of_4)
    circle4 = Circles(x_of_4, y_of_4, r4) # 4th circle created here
    circle1 = outerTangCirc(circle2, circle3, circle4) # Function calls outerTangCirc(function) to create external circle
    return (circle1, circle2, circle3, circle4)

def secSolution(fixedCirc, circle1, circle2, circle3): # Function that is able to generate circles based on known information on existing circles
    curvF = fixedCirc.curvature()
    curv1 = circle1.curvature()
    curv2 = circle2.curvature()
    curv3 = circle3.curvature()

    # Variation of Vieta's formula
    newCurv = 2*(curv1 + curv2 + curv3) - curvF
    newPos = (2*(curv1*circle1.pos + curv2*circle2.pos + curv3*circle3.pos) - curvF*fixedCirc.pos)/newCurv
    return Circles(newPos.real, newPos.imag, 1/newCurv)
        
class containGasket(): # Class contains list containing all calculated and generated information on the circle objects

    def __init__(self, circle1, circle2, circle3, circle4):
        self.start = innerTangCirc(circle1, circle2, circle3) # Start with 3 known tangent circles and the enclosing circle
        self.generate = list(self.start) # Start list of objects with 3 known tangent circles

    def ApolloGasket(self, circles, depth, maxDepth): # Generation and recursive calls are made here
        if depth == maxDepth: # Stop if the max depth has been reached
            return
        (circle1, circle2, circle3, circle4) = circles
        if depth == 0: # First depth requires creation of the enclosed circle
            specialCirc = secSolution(circle1, circle2, circle3, circle4)
            self.generate.append(specialCirc)
            self.ApolloGasket((specialCirc, circle2, circle3, circle4), 1, maxDepth) # Recursive call for next depth

        newCircle2 = secSolution(circle2, circle1, circle3, circle4) # Three circles can be generated based off of which circle is "fixed"
        self.generate.append(newCircle2)                             # For depth "n" we get total of 2*3^(n+1) circles
        newCircle3 = secSolution(circle3, circle1, circle2, circle4)
        self.generate.append(newCircle3)
        newCircle4 = secSolution(circle4, circle1, circle2, circle3)
        self.generate.append(newCircle4)

        self.ApolloGasket((newCircle2, circle1, circle3, circle4), depth + 1, maxDepth) # Recursive call for next depth
        self.ApolloGasket((newCircle3, circle1, circle2, circle4), depth + 1, maxDepth) # Three circles generated means three calls to be made
        self.ApolloGasket((newCircle4, circle1, circle2, circle3), depth + 1, maxDepth)
def draw(colourlist,skycolour,screen):
    global r1
    global r2
    global r3
    global randX
    global randY
    global cls
    pygame.draw.rect(screen, skycolour, (123,217,435,200))

    MOON = colourlist
    cls = []
    
    largestRad = 0
    r1 = random.randrange(10,30)
    r2 = random.randrange(10,30)
    r3 = random.randrange(10,30)                                     
    randX = random.randrange(153, 420)
    randY = random.randrange(260, 290)

    # Calculations using Vieta's formula to find 3 tangent circles
    test1 = Circles(randX, randY, r1)
    test2 = Circles(randX + r1 + r2, 100, r2)
    x3 = randX + (r1*r1 + r1*r3 + r1*r2 - r2*r3)/(r1+r2)
    y3 = randY + cmath.sqrt(((r1+r3)*(r1+r3)) - (r1*r1 + r1*r3 + r1*r2 - r2*r3)/(r1+r2)*(r1*r1 + r1*r3 + r1*r2 - r2*r3)/(r1+r2))
    test3 = Circles(x3, y3, r3)

    # Keep track of the largest radius (has to be the enclosing circle), largest circle must be drawn first 
    largestRad = math.fabs(outerTangCirc(test1, test2, test3).r.real)
    stuff = containGasket(test1, test2, test3, outerTangCirc(test1, test2, test3)) # Create the Apollo Gasket list of Circles objects
    stuff.ApolloGasket(stuff.generate, 0, 6) # Base recursion call

    # [Moon]:
    for current in stuff.generate:
        if 0 < int(math.fabs(current.r.real)) < math.fabs(largestRad): # Draws all circles that have a radius over 1, and under the largest radius
            cls.append(random.randrange(len(MOON)))
            pygame.draw.circle(screen, MOON[cls[-1]], (randX + int(current.pos.real), randY + int(current.pos.imag)), int(math.fabs(current.r.real)), 0)
    # Pygame does not support float radius, because of this, once circles get small enough, the rounding may cause circles to no longer appear tangent to one another
    pygame.display.update()

def redraw(colourlist,skycolour,screen):
    global r1
    global r2
    global r3
    global randX
    global randY
    global cls
    pygame.draw.rect(screen, skycolour, (123,217,435,200))
    MOON = colourlist
    counter = 0

    # Calculations using Vieta's formula to find 3 tangent circles
    test1 = Circles(randX, randY, r1)
    test2 = Circles(randX + r1 + r2, 100, r2)
    x3 = randX + (r1*r1 + r1*r3 + r1*r2 - r2*r3)/(r1+r2)
    y3 = randY + cmath.sqrt(((r1+r3)*(r1+r3)) - (r1*r1 + r1*r3 + r1*r2 - r2*r3)/(r1+r2)*(r1*r1 + r1*r3 + r1*r2 - r2*r3)/(r1+r2))
    test3 = Circles(x3, y3, r3)

    # Keep track of the largest radius (has to be the enclosing circle), largest circle must be drawn first 
    largestRad = math.fabs(outerTangCirc(test1, test2, test3).r.real)
    stuff = containGasket(test1, test2, test3, outerTangCirc(test1, test2, test3)) # Create the Apollo Gasket list of Circles objects
    stuff.ApolloGasket(stuff.generate, 0, 6) # Base recursion call

    # [Moon]:
    for current in stuff.generate:
        if 0 < int(math.fabs(current.r.real)) < math.fabs(largestRad): # Draws all circles that have a radius over 1, and under the largest radius
            pygame.draw.circle(screen, MOON[cls[counter]], (randX + int(current.pos.real), randY + int(current.pos.imag)), int(math.fabs(current.r.real)), 0)
            counter += 1
    # Pygame does not support float radius, because of this, once circles get small enough, the rounding may cause circles to no longer appear tangent to one another
    pygame.display.update()
    
           
           
