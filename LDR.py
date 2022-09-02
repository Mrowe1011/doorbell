from email import message
import RPi.GPIO as GPIO
import time
import pymsteams
GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the circuit
pin_to_circuit = 7
blipper = 0
def GeneralLogic():
    sendDoor()

def sendDoor():
    global blipper
    myTeamsMessage = pymsteams.connectorcard("APIkeyHere")

    if blipper > 2:
        myTeamsMessage.text("Messages sent in a row exceeded 3, pausing for 2 minutes.")
        print("Messages sent in a row exceeded 3, pausing for 2 minutes.")
        time.sleep(120)
        # reset the cooldown variable
        blipper = 0
    else:
        myTeamsMessage.text("Someone walked through the door!")
        print("normal message sent")
        # send the message.
        myTeamsMessage.send()

        # blipper stores the cooldown varable so it doesn't spam.
        blipper = blipper + 1
        # Cool down of 30 seconds after beam is tripped so it doesn't repeat for one person.
        time.sleep(30)

    
    print(blipper)


def rc_time (pin_to_circuit):
    #Count counts the cycles it takes to charge the capacitor
    count = 0
    global blipper
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1
    print(count)
    if count < 500:
        message = "nothing there"
        blipper = 0
    else:
        GeneralLogic()
        message = "ding"
    return message

#Catch when script is interrupted, cleanup correctly
try:
    # Main loop
    while True:
        time.sleep(1)
        print(rc_time(pin_to_circuit))
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()