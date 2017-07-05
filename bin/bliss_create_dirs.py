#!/usr/bin/env python

'''
Usage:
    bliss-create-dirs [options]

Arguments:

    -d DATETIME, --datetime=<YYYY-MM-DDTHH:mm:ssZ>  Create directory structure using this
                                                    ISO 8601 datetime for strftime replacement
                                                    in directory path. Default: TODAY

Description:

    BLISS Create Directory Structure

    Based on the data paths specified in the BLISS_CONFIG, this software creates
    daily directories for the GDS based on the paths and any applicable variable
    substitution.

    Define the Paths
    ================

    Paths should be specified within the 'data' portion of the BLISS_CONFIG. It
    should follow the following hierarchy within the YAML file:

        data:
            data-type:
                path:

    For example:

        data:
            type_a:
                path: /path/to/data/type_a
            type_b:
                path: /path/to/data/type_b

    Be sure to use 'path' to specify the data path so the software knows to
    translate these paths as needed. You can use absolute or relative paths:

        data:
            type_a:
                path: to/data/type_a
            type_b:
                path: ~/to/data/type_b


    Variable Substitution
    =====================

    Variable substituion is also possible using any of the default-, platform-,
    or host- level attributes within the BLISS_CONFIG. To include a variable
    in a path use the following syntax, `${variable}`

    For example,

        default:
            mission: 'oco3'
            phase: 'int'

            data:
                type_a:
                    path: /${mission}/${phase}/data/type_a
                type_b:
                    path: /${mission}/${phase}/data/type_b

    Will create the directories:

        /oco3/int/data/type_a
        /oco3/int/data/type_b


    Special Variables and strftime directives
    =========================================

    There are also several special variables available:
    * hostname = current machine hostname
    * platform = platform of the current machine (darwin, win32, etc.)

    You can also use `strftime format characters
    <https://docs.python.org/2/library/time.html#time.strftime>`.

    For example,

        default:
            mission: 'oco3'
            phase: 'int'

            data:
                type_a:
                    path: /${mission}/${phase}/%Y/%Y-%j/type_a
                type_b:
                    path: /${mission}/${phase}/%Y/%Y-%j/type_b

    Will produce paths like (depending on the date):

        /oco3/int/2016/2016-299/type_a
        /oco3/int/2016/2016-299/type_b


'''

import os
import errno
import traceback
import yaml
import argparse
import time

import bliss
from bliss.core import dmc, log


def createDirStruct(paths, verbose=True):
    '''Loops bliss.config._datapaths from BLISS_CONFIG and creates a directory.

    Replaces year and doy with the respective year and day-of-year.
    If neither are given as arguments, current UTC day and year are used.

    Args:
        paths:
            [optional] list of directory paths you would like to create.
            doy and year will be replaced by the datetime day and year, respectively.

        datetime:
            UTC Datetime string in ISO 8601 Format YYYY-MM-DDTHH:mm:ssZ

    '''
    for k, path in paths.items():
        p = None
        try:
            pathlist = path if type(path) is list else [ path ]
            for p in pathlist:
                os.makedirs(p)
                if verbose:
                    log.info('Creating directory: ' + p)
        except OSError, e:
            #print path
            if e.errno == errno.EEXIST and os.path.isdir(p):
                pass
            else:
                raise

    return True

def main():

    argparser = argparse.ArgumentParser(
        description = """
    BLISS Create Directories Script

    Based on the data paths specified in the BLISS_CONFIG, this software creates
    daily directories for the GDS based on the paths and any applicable variable
    substitution.
""",
        epilog = """
    Create directories based on some set of variables in a separate YAML config

        $ bliss-create-dirs -c vars.yaml

    Create directories starting 3 days from now for 90 days

        $ bliss-create-dirs -d 2016-01-01T00:00:00Z
""",
        formatter_class = argparse.RawDescriptionHelpFormatter
    )

    argparser.add_argument(
        '-d', '--date',
        metavar = '<YYYY-MM-DDTHH:mm:ssZ>',
        type    = str,
        help    = 'Create directory structure using this' +
                    'ISO 8610 datetime for strftime replacement' +
                    'in directory path. Default: TODAY'
    )

    argparser.add_argument(
        '-t', '--timedelta',
        metavar = '<days>',
        type    = int,
        help    = 'Number of days in the future you would like '+
                    'to create a directory.' +
                    'Default: 0'
    )

    options = argparser.parse_args()

    log.begin()

    retcode = 0

    try:
        pathvars = { }

        if options.date:
            bliss.config._datetime = time.strptime(options.date, dmc.ISO_8601_Format)

        if options.timedelta:
            bliss.config._datetime = time.strptime(dmc.getUTCDatetimeDOY(days=options.timedelta),
                dmc.DOY_Format)

        pathvars['year'] = bliss.config._datetime.tm_year
        pathvars['doy'] = '%03d' % bliss.config._datetime.tm_yday
        
        # Add the updated path variables for the date
        bliss.config.addPathVariables(pathvars)

        bliss.config.reload()

        # Create the directory
        retcode = createDirStruct(bliss.config._datapaths)

    except Exception as e:
        print e
        log.error('BLISS Create Directories error: %s' % traceback.format_exc())

    log.end()
    return retcode

if __name__ == '__main__':
    main()
