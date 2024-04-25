from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys
import markdownify
import urllib.parse
import urllib.error # ANDF TEST
import re as regex
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--local', action='store_true', required=False)
parser.add_argument("flutter", help="Run against Flutter SDK only.")
parser.add_argument("-v", "--verbose", help="Run with increased output verbosity.",
                    action="store_true", required=False)
                    
args = parser.parse_args()

sdk_url_mapping = {
    "go": "https://pkg.go.dev/go.viam.com/rdk",
    "python": "https://python.viam.dev",
    "cpp": "https://cpp.viam.dev",
    "typescript": "https://ts.viam.dev",
    "flutter": "https://flutter.viam.dev"
}

components = ["arm", "base", "board", "camera", "encoder", "gantry", "generic_component", "gripper",
              "input_controller", "motor", "movement_sensor", "power_sensor", "sensor"]
services = ["generic_service", "mlmodel", "motion", "navigation", "slam", "vision"]
app_apis = ["app", "data", "mltraining"]
robot_apis = ["robot"]

proto_map = {
    "arm": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/arm/v1/arm_grpc.pb.go",
        "name": "ArmServiceClient",
        "methods": []
    },
    "base": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/base/v1/base_grpc.pb.go",
        "name": "BaseServiceClient",
        "methods": []
    },
    "board": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/board/v1/board_grpc.pb.go",
        "name": "BoardServiceClient",
        "methods": []
    },
    "camera": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/camera/v1/camera_grpc.pb.go",
        "name": "CameraServiceClient",
        "methods": []
    },
    "encoder": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/encoder/v1/encoder_grpc.pb.go",
        "name": "EncoderServiceClient",
        "methods": []
    },
    "gantry": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/gantry/v1/gantry_grpc.pb.go",
        "name": "GantryServiceClient",
        "methods": []
    },
    "generic_component": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/generic/v1/generic_grpc.pb.go",
        "name": "GenericServiceClient",
        "methods": []
    },
    "gripper": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/gripper/v1/gripper_grpc.pb.go",
        "name": "GripperServiceClient",
        "methods": []
    },
    "input_controller": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/inputcontroller/v1/input_controller_grpc.pb.go",
        "name": "InputControllerServiceClient",
        "methods": []
    },
    "motor": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/motor/v1/motor_grpc.pb.go",
        "name": "MotorServiceClient",
        "methods": []
    },
    "movement_sensor": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/movementsensor/v1/movementsensor_grpc.pb.go",
        "name": "MovementSensorServiceClient",
        "methods": []
    },
    "power_sensor": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/powersensor/v1/powersensor_grpc.pb.go",
        "name": "PowerSensorServiceClient",
        "methods": []
    },
    "sensor": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/component/sensor/v1/sensor_grpc.pb.go",
        "name": "SensorServiceClient",
        "methods": []
    },
    "generic_service": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/service/generic/v1/generic_grpc.pb.go",
        "name": "GenericServiceClient",
        "methods": []
    },
    "mlmodel": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/service/mlmodel/v1/mlmodel_grpc.pb.go",
        "name": "MLModelServiceClient",
        "methods": []
    },
    "motion": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/service/motion/v1/motion_grpc.pb.go",
        "name": "MotionServiceClient",
        "methods": []
    },
    "navigation": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/service/navigation/v1/navigation_grpc.pb.go",
        "name": "NavigationServiceClient",
        "methods": []
    },
    "slam": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/service/slam/v1/slam_grpc.pb.go",
        "name": "SLAMServiceClient",
        "methods": []
    },
    "vision": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/service/vision/v1/vision_grpc.pb.go",
        "name": "VisionServiceClient",
        "methods": []
    },
    "app": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/app/v1/app_grpc.pb.go",
        "name": "AppServiceClient",
        "methods": []
    },
    "data": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/app/data/v1/data_grpc.pb.go",
        "name": "DataServiceClient",
        "methods": []
    },
    "robot": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/robot/v1/robot_grpc.pb.go",
        "name": "RobotServiceClient",
        "methods": []
    },
    "mltraining": {
        "url": "https://raw.githubusercontent.com/viamrobotics/api/main/app/mltraining/v1/ml_training_grpc.pb.go",
        "name": "MLTrainingServiceClient",
        "methods": []
    }
}

flutter_resource_overrides = {
    "generic_component": "generic",
    "movement_sensor": "movementsensor",
    "power_sensor": "powersensor",
    "generic_service": "generic",
    "mltraining": "ml_training"
}

def get_proto_apis():
    for api in proto_map.keys():
        api_url = proto_map[api]["url"]
        api_name = proto_map[api]["name"]

        api_page = urlopen(api_url)
        api_html = api_page.read().decode("utf-8")

        my_regex = 'type ' + regex.escape(api_name) + '[^{]*\{([^}]+)\}'
        search = regex.search(my_regex, api_html)
        match_output = search.group()
        split = match_output.splitlines()

        for line in split:
            line = line.strip()
            if line[0].isupper():
                separator = "("
                line = line.split(separator, 1)[0]
                proto_map[api]["methods"].append(line)
   
    return proto_map

def make_soup(url):
   try:
       page = urlopen(url)
       html = page.read().decode("utf-8")
       return BeautifulSoup(html, "html.parser")
   except urllib.error.HTTPError as err:
       print(f'An HTTPError was thrown: {err.code} {err.reason} for URL: {url}')

def parse(type, names):

## TODO:
## - Not fetching returns when > 1 return exists. This works with params; adapt. Or: do we even have methods with multiple returns?
## - Probably considering a or non-a returns too early, consider within for loop.
## - Not yet handling no returns yet, required.
## - Not yet fetching param or param type descriptions, required.
## - Spot check of methods across all resource reveals a few missing, investigate, if not captured by above TODOs.

    if args.flutter:

        flutter_methods = {}
        flutter_methods[type] = {}

        sdk_url = sdk_url_mapping["flutter"]

        for resource in names:
            if resource in flutter_resource_overrides:
                url = f"{sdk_url}/viam_protos.{type}.{flutter_resource_overrides[resource]}/{proto_map[resource]['name']}-class.html"
            else:
                url = f"{sdk_url}/viam_protos.{type}.{resource}/{proto_map[resource]['name']}-class.html"

            flutter_methods[type][resource] = {}

            soup = make_soup(url)

            ## Limit matched class to exactly 'callable', i.e. not 'callable inherited', remove the constructor (proto id) itself, and remove '*_Pre' methods from Robot API:
            flutter_methods_raw = soup.find_all(
                lambda tag: tag.name == 'dt'
                and tag.get('class') == ['callable']
                and not regex.search(proto_map[resource]['name'], tag.text)
                and not regex.search('_Pre', tag.text))

            for tag in flutter_methods_raw:

                this_method_dict = {}

                method_name = tag.get('id')
                this_method_dict["method_link"] = tag.find("span", class_="name").a['href'].replace("..", sdk_url)

                parameters_link = tag.find("span", class_="type-annotation").a['href'].replace("..", sdk_url)
                parameters_soup_raw = make_soup(parameters_link)
                parameters_soup = parameters_soup_raw.find_all(
                    lambda tag: tag.name == 'dt'
                    and tag.get('class') == ['property']
                    and not regex.search('info_', tag.text))

                this_method_dict["parameters"] = {}
                this_method_parameters_dict = {}
                this_method_dict["returns"] = {}
                this_method_returns_dict = {}

                # Parse parameters:
                for parameter_tag in parameters_soup:

                    param_name = parameter_tag.get('id')
                    this_method_parameters_dict["param_link"] = parameter_tag.find("span", class_="name").a['href'].replace("..", sdk_url)

                    parameter_type_raw = parameter_tag.find("span", class_="signature")

                    if not parameter_type_raw.find("a"):
                        this_method_parameters_dict["param_type"] = parameter_type_raw.string[2:]
                    elif len(parameter_type_raw.find_all("a")) == 1:
                        this_method_parameters_dict["param_type"] = parameter_type_raw.find("a").text
                        this_method_parameters_dict["param_type_link"] = parameter_type_raw.a['href'].replace("..", sdk_url)
                    elif len(parameter_type_raw.find_all("a")) == 2:
                        this_method_parameters_dict["param_type"] = parameter_type_raw.find("a").text
                        this_method_parameters_dict["param_type_link"] = parameter_type_raw.a['href'].replace("..", sdk_url)
                        this_method_parameters_dict["param_subtype"] = parameter_type_raw.find("span", class_="type-parameter").text
                        this_method_parameters_dict["param_subtype_link"] = parameter_type_raw.find("span", class_="type-parameter").a['href'].replace("..", sdk_url)

                    this_method_dict["parameters"][param_name] = this_method_parameters_dict

                # Parse returns:
                if tag.find("span", class_="type-parameter").a:

                    returns_link = tag.find("span", class_="type-parameter").a['href'].replace("..", sdk_url)
                    returns_soup_raw = make_soup(returns_link)
                    returns_soup = returns_soup_raw.find_all(
                        lambda tag: tag.name == 'dt'
                        and tag.get('class') == ['property']
                        and not regex.search('info_', tag.text))

                    for return_tag in returns_soup:
                        return_name = return_tag.get('id')
                        this_method_returns_dict["return_link"] = return_tag.find("span", class_="name").a['href'].replace("..", sdk_url)

                        return_type_raw = return_tag.find("span", class_="signature")

                        if not return_type_raw.find("a"):
                            this_method_returns_dict["return_type"] = return_type_raw.string[2:]
                        elif len(return_type_raw.find_all("a")) == 1:
                            this_method_returns_dict["return_type"] = return_type_raw.find("a").text
                            this_method_returns_dict["return_type_link"] = return_type_raw.a['href'].replace("..", sdk_url)
                        elif len(return_type_raw.find_all("a")) == 2:
                            this_method_returns_dict["return_type"] = return_type_raw.find("a").text
                            this_method_returns_dict["return_type_link"] = return_type_raw.a['href'].replace("..", sdk_url)
                            this_method_returns_dict["return_subtype"] = return_type_raw.find("span", class_="type-parameter").text
                            this_method_returns_dict["return_subtype_link"] = return_type_raw.find("span", class_="type-parameter").a['href'].replace("..", sdk_url)

                        this_method_dict["returns"][return_name] = this_method_returns_dict

                else:
                    return_name = return_tag.get('id')
                    this_method_returns_dict["return_type"] = tag.find("span", class_="type-parameter").string

                flutter_methods[type][resource][method_name] = this_method_dict

    #print(flutter_methods)
    return flutter_methods


## TODO:
## This is where we define our markdownify function.
## - Separated from `parse()`, with goal of being as language-agnostic as possible: parse per-language (for now) with markdownify universal.
## - Accepts a dict-of-dicts object as param, writes resulting markdown, returns nothing (besides maybe debug status)
##
## Fun pseudocode (i.e. you don't have to map dict[index] to var explicitly, you can just use them inline in the markdownification steps directly):
##
## ## Iterate by types, like 'component':
## for type in passed_methods.keys():
##     ## Iterate by resource, like 'arm':
##     for resource in type.keys():
##         ## Iterate by method, like 'doCommand'
##         for method in resource.keys()
##             method_link = method[1]
##             ## Iterate by parameter, like 'command':
##             for parameter in method[parameters].keys()
##                 parameter_name = parameter
##                 parameter_link = parameter[param_link]
##                 parameter_type_link = parameter[param_type_link]
##                 ## Determine if this param type has subtypes, like map(string):
##                 if param-has-subtypes:
##                     param_subtype = parameter[param_subtype]
##                     param_subtype_link = parameter[param_subtype_link]
##             if method-has-returns:
##                 for return in method[returns].keys()
##                     return_name = return
##                     return_link = return[return_link]
##                     return_type = return[return_type]
##                     return_type_link = return[return_type_link]
##                     if param-has-subtypes:
##                         return_subtype = return[return_subtype]
##                         return_subtype_link = return[return_subtype_link]



## TODO:
## Consider restructuring existing `docs` repo to support easier inline-replace of content.
## ANDF investigating
## Requirements:
## - Must support arbitrary manual copy in addition to automated content, example:
##   https://docs.viam.com/components/camera/#getimages



## Temporary holding main function to:
## - Fetch canonical proto methods from upstream, used for mapping in `parse()`
## - Get methods for each defined type & resource
## - Simple print for each dict during script development
def run():

    proto_map = get_proto_apis()

    component_methods = parse("component", components)
    ## Here's where we would markdownify(component_methods)
    print(component_methods)

    service_methods = parse("service", services)
    ## Here's where we would markdownify(service_methods)
    print(service_methods)

    app_methods = parse("app", app_apis)
    ## Here's where we would markdownify(app_methods)
    print(app_methods)

    robot_methods = parse("robot", robot_apis)
    ## Here's where we would markdownify(robot_methods)
    print(robot_methods)

run()

sys.exit(1)
