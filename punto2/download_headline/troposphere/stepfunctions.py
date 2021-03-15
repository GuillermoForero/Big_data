# Copyright (c) 2012-2019, Mark Peek <mark@peek.org>
# All rights reserved.
#
# See LICENSE file for full license.
#
# *** Do not modify - this file is autogenerated ***
# Resource specification version: 10.0.0


from . import AWSObject
from . import AWSProperty
from troposphere import Tags
from .validators import boolean


class Activity(AWSObject):
    resource_type = "AWS::StepFunctions::Activity"

    props = {
        'Name': (str, True),
        'Tags': (Tags, False),
    }


class CloudWatchLogsLogGroup(AWSProperty):
    props = {
        'LogGroupArn': (str, True),
    }


class LogDestination(AWSProperty):
    props = {
        'CloudWatchLogsLogGroup': (CloudWatchLogsLogGroup, False),
    }


class LoggingConfiguration(AWSProperty):
    props = {
        'Destinations': ([LogDestination], False),
        'IncludeExecutionData': (boolean, False),
        'Level': (str, False),
    }


class S3Location(AWSProperty):
    props = {
        'Bucket': (str, True),
        'Key': (str, True),
        'Version': (str, False)
    }


class TracingConfiguration(AWSProperty):
    props = {
        'Enabled': (boolean, False),
    }


class StateMachine(AWSObject):
    resource_type = "AWS::StepFunctions::StateMachine"

    props = {
        'DefinitionS3Location': (S3Location, False),
        'DefinitionString': (str, False),
        'DefinitionSubstitutions': (dict, False),
        'LoggingConfiguration': (LoggingConfiguration, False),
        'RoleArn': (str, True),
        'StateMachineName': (str, False),
        'StateMachineType': (str, False),
        'Tags': (Tags, False),
        'TracingConfiguration': (TracingConfiguration, False),
    }