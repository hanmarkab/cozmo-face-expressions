import cozmo
import time
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.util import degrees, distance_mm, speed_mmps

def cozmo_program(robot: cozmo.robot.Robot):
    #Find a face

    robot.set_lift_height(0,2,2).wait_for_completed()
    robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
    robot.say_text("Hi I am Cozmo, I am looking for a friend").wait_for_completed()
    try:
        myFace = robot.world.wait_for_observed_face(timeout=30)
    except asyncio.TimeoutError:
        print("Didn't find a face - exiting!")
        return
    robot.say_text("Found a friend").wait_for_completed()

    #Estimate expression
    robot.enable_facial_expression_estimation(enable=True)
    Fexpress = myFace.expression
    print(Fexpress)
    if Fexpress == "happy":
        robot.say_text("You are happy").wait_for_completed()
    elif Fexpress == "neutral":
        robot.say_text("You are neutral").wait_for_completed()
    elif Fexpress == "surprised":
        robot.say_text("You are surprised").wait_for_completed()
    elif Fexpress == "angry":
        robot.say_text("You are angry").wait_for_completed()
    elif Fexpress == "sad":
        robot.say_text("You are sad").wait_for_completed()
    elif Fexpress == "unknown":
        robot.say_text("I can't tell your emotion right now").wait_for_completed()
    else:
        robot.say_text("Hello").wait_for_completed()


    if Fexpress == "happy":
        robot.say_text("Do you want to be friends? We can play with my block together").wait_for_completed()
        lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        cubes = robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube, timeout=60)
        lookaround.stop()
        print(len(cubes))
        if(len(cubes) > 0):
            current_action = robot.pickup_object(cubes[0], num_retries=3)
            current_action.wait_for_completed()
            if current_action.has_failed:
                code, reason = current_action.failure_reason
                result = current_action.result
                print("Pickup Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
                return
            robot.drive_straight(distance_mm(150), speed_mmps(50)).wait_for_completed()
            thisaction = robot.place_object_on_ground_here(cubes[0], num_retries = 3)
            thisaction.wait_for_completed()
            robot.say_text("Best Friends forever").wait_for_completed()
    elif Fexpress == "neutral":
        robot.say_text("You look like you are in a bad mood, can I cheer you up?").wait_for_completed()
        robot.play_anim_trigger(cozmo.anim.Triggers.RollBlockSuccess).wait_for_completed()
        robot.play_anim_trigger(cozmo.anim.Triggers.Singing_120bpm).wait_for_completed()
    elif Fexpress == "surprised":
        robot.say_text("If you think that's cool, look what I can do!").wait_for_completed()
        lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        cubes = robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube, timeout=60)
        lookaround.stop()
        print(len(cubes))
        if(len(cubes) > 0):
            action = robot.pop_a_wheelie(cubes[0], num_retries=2).wait_for_completed()
        robot.say_text("Boo yah!").wait_for_completed()
        robot.play_anim_trigger(cozmo.anim.Triggers.FlipDownFromBack).wait_for_completed()
    elif Fexpress == "angry":
        robot.say_text("You look like you are in a bad mood, can I cheer you up?").wait_for_completed()
        robot.play_anim_trigger(cozmo.anim.Triggers.RollBlockSuccess).wait_for_completed()
        robot.play_anim_trigger(cozmo.anim.Triggers.Singing_120bpm).wait_for_completed()
    elif Fexpress == "sad":
        robot.say_text("You look like you are in a bad mood, can I cheer you up?").wait_for_completed()
        robot.play_anim_trigger(cozmo.anim.Triggers.RollBlockSuccess).wait_for_completed()
        robot.play_anim_trigger(cozmo.anim.Triggers.Singing_120bpm).wait_for_completed()
    elif Fexpress == "unknown":
        robot.say_text("This person's looking shifty.").wait_for_completed()
        lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        cubes = robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube, timeout=60)
        lookaround.stop()
        print(len(cubes))
        if(len(cubes) > 0):
            current_action = robot.pickup_object(cubes[0], num_retries=3)
            current_action.wait_for_completed()
            if current_action.has_failed:
                code, reason = current_action.failure_reason
                result = current_action.result
                print("Pickup Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
                return
            robot.say_text("Stranger").wait_for_completed()
            robot.drive_straight(distance_mm(-50), speed_mmps(20)).wait_for_completed()
            robot.say_text("Danger").wait_for_completed()
            robot.drive_straight(distance_mm(-200), speed_mmps(70)).wait_for_completed()

    else:
        robot.say_text("Hello").wait_for_completed()

        # Try and pickup the 1st cube
#        current_action = robot.pickup_object(cubes[0], num_retries=3)
#        current_action.wait_for_completed()
#        if current_action.has_failed:
#            code, reason = current_action.failure_reason
#            result = current_action.result
#            print("Pickup Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
#            return
#
#        robot.say_text("I picked it up").wait_for_completed()
#        current_action = robot.place_object_on_ground_here(cubes[0], num_retries = 3)
#        current_action.wait_for_completed()
#        robot.say_text("All done!")

cozmo.run_program(cozmo_program)
