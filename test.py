import cozmo
import time
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.util import degrees, distance_mm, speed_mmps

def resetCozmo(robot: cozmo.robot.Robot):
    '''
    Resets Cozmo's lift and head to a neutral position
    '''
    robot.set_lift_height(0,2,2).wait_for_completed()
    robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()

def getVisibleFace(robot: cozmo.robot.Robot):
    '''
    Returns the first visible face Cozmo sees, or 'None' if no face was seen
    '''
    observedFace = None
    try:
        observedFace = robot.world.wait_for_observed_face(timeout=30)
    except asyncio.TimeoutError:
        print("Didn't find a face - exiting!")
        return None
    return observedFace

def getFacialExpression(robot: cozmo.robot.Robot):
    '''
    Returns an estimate of the expression of Cozmo's first observed face
    '''
    observedFace = getVisibleFace(robot)
    if observedFace == None:
        return None
    robot.enable_facial_expression_estimation(enable=True)
    facialExpression = observedFace.expression
    return facialExpression

def isFaceKnown(robot: cozmo.robot.Robot, face: cozmo.faces.Face):
    '''
    Returns if the face is known or not
    '''
    if not face.name:
        robot.say_text("I don't recognize you").wait_for_completed()
        return False
    robot.say_text("Hello %s!" % (face.name)).wait_for_completed()
    return True

def sayFacialExpression(robot: cozmo.robot.Robot, facialExpression: str):
    '''
    Cozmo speaks the given facial expression out loud
    '''
    if facialExpression == "happy":
        robot.say_text("You are happy").wait_for_completed()
    elif facialExpression == "neutral":
        robot.say_text("You are neutral").wait_for_completed()
    elif facialExpression == "surprised":
        robot.say_text("You are surprised").wait_for_completed()
    elif facialExpression == "angry":
        robot.say_text("You are angry").wait_for_completed()
    elif facialExpression == "sad":
        robot.say_text("You are sad").wait_for_completed()
    elif facialExpression == "unknown":
        robot.say_text("I can't tell your emotion right now").wait_for_completed()
    else:
        robot.say_text("Hello").wait_for_completed()

def findVisibleCubes(robot: cozmo.robot.Robot, lookAround: bool = True, 
        numCubes: float = 1, searchTimeout: float = 60):
    '''
    Cozmo searches in-place for visible cubes
    '''
    if lookAround:
        lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)

    foundCubes = robot.world.wait_until_observe_num_objects(num = numCubes,
            object_type = cozmo.objects.LightCube, timeout = searchTimeout)

    if lookAround:
        lookaround.stop()
    return foundCubes

def pickupCube(robot: cozmo.robot.Robot, cube: cozmo.objects.LightCube, 
        numRetries: float = 3):
    '''
    Cozmo tries to pick up the given cube, trying at least 'numRetries' times
    before giving up
    '''
    current_action = robot.pickup_object(cube, num_retries = numRetries)
    current_action.wait_for_completed()
    if current_action.has_failed:
        code, reason = current_action.failure_reason
        result = current_action.result
        print("Pickup Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
        return

def findAndGiveCubeToFriend(robot: cozmo.robot.Robot):
    '''
    Cozmo acts happily by trying to find a cube to share with someone, picking
    it up, and giving it to them
    '''
    robot.say_text("Do you want to be friends? We can play with my block together").wait_for_completed()

    cubes = findVisibleCubes(robot)
    print(len(cubes))

    if len(cubes) > 0:
        pickupCube(robot, cubes[0])
        
        robot.drive_straight(distance_mm(150), speed_mmps(50)).wait_for_completed()
        thisaction = robot.place_object_on_ground_here(cubes[0])
        thisaction.wait_for_completed()

        robot.say_text("Best Friends forever").wait_for_completed()
    else:
        robot.say_text("Aw, I can't show you my block")

def impressFriendUsingWheelie(robot: cozmo.robot.Robot):
    '''
    Cozmo tries to pick up a cube and use it to do a wheelie
    '''
    robot.say_text("If you think that's cool, look what I can do!").wait_for_completed()

    cubes = findVisibleCubes(robot)
    print(len(cubes))

    if len(cubes) > 0:
        action = robot.pop_a_wheelie(cubes[0], num_retries=2).wait_for_completed()
    robot.say_text("Boo yah!").wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.FlipDownFromBack).wait_for_completed()

def cheerFriendUp(robot: cozmo.robot.Robot):
    '''
    Cozmo will try to cheer the person up by doing a spritely dance and singing
    '''
    robot.say_text("You look like you are in a bad mood, can I cheer you up?").wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.RollBlockSuccess).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.Singing_120bpm).wait_for_completed()

def runAwayFromStranger(robot: cozmo.robot.Robot):
    '''
    Cozmo finds the first cube he sees, picks it up, and drives in the opposite
    direction
    '''
    robot.say_text("This person's looking shifty.").wait_for_completed()
    
    cubes = findVisibleCubes(robot)
    print(len(cubes))

    if len(cubes) > 0:
        pickupCube(robot, cubes[0])

        robot.say_text("Stranger").wait_for_completed()
        robot.drive_straight(distance_mm(-50), speed_mmps(20)).wait_for_completed()
        robot.say_text("Danger").wait_for_completed()
        robot.drive_straight(distance_mm(-200), speed_mmps(70)).wait_for_completed()

def reactToFacialExpression(robot: cozmo.robot.Robot, Fexpress: str):
    '''
    Cozmo takes an appropriate action based on the observed facial expression
    '''
    if Fexpress == "happy":
        findAndGiveCubeToFriend(robot)
    elif Fexpress == "surprised":
        impressFriendUsingWheelie(robot)
    elif Fexpress == "neutral" or Fexpress == "angry" or Fexpress == "sad":
        cheerFriendUp(robot)
    elif Fexpress == "unknown":
        print("Unknown expression")
        Fexpress = getFacialExpression(robot)
        reactToFacialExpression(robot, Fexpress)
    else:
        robot.say_text("Hello").wait_for_completed()

def cozmo_program(robot: cozmo.robot.Robot):

    resetCozmo(robot)
    robot.say_text("Hi I am Cozmo, I am looking for a friend").wait_for_completed()

    #Find a face / Estimate expression
    Fexpress = getFacialExpression(robot)
    print(Fexpress)

    if Fexpress:
        robot.say_text("Found a Friend").wait_for_completed()

    reactToFacialExpression(robot, Fexpress)

#=========== Below portion is what actually runs the above program =============

cozmo.run_program(cozmo_program)
