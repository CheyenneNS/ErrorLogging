import re
import ast
import error_categories_EE2
import pprint

def filter_error(error, errlog_dictionary):

    delimiters = "{", "}", "''", ":", ",", "message"
    regexPattern = '|'.join(map(re.escape, delimiters))
    if error[0] == error[-1] == "'":
        if len(error) == 2:
            errlog_dictionary["error"] = "_NULL_"
            errlog_dictionary["err_prefix"] = "_NULL_"
            errlog_dictionary["category"] = "_NULL_"
        else:
            error = error[1:-1].strip()
            prefix = re.split(regexPattern, error)
            prefix = list(filter(lambda s: any([c.isalnum() for c in s]), prefix))[0]
            err_prefix = re.sub(r'([\'"{}\\><*])', '', prefix).replace("(", ' ').replace("[", '').strip()
            # Update error dictionary for error and append to logs
            errlog_dictionary["error"] = error
            errlog_dictionary["err_prefix"] = err_prefix
            category = error_categories_EE2.add_category(errlog_dictionary)
            errlog_dictionary["category"] = category

    elif error[0] == error[-1] == '"':
        error = error[1:-1].strip()
        # Errors that end in double quotes can be wrapping single qoutes
        if error[0] == error[-1] == "'":
            error = error[1:-1]
            prefix = re.split(regexPattern, error)
            prefix = list(filter(lambda s: any([c.isalnum() for c in s]), prefix))[0]
            err_prefix = re.sub(r'([\'"{}\\><*])', '', prefix).replace("(", ' ').replace("[", '').strip()
        # Error can be tuple wrapped in string
        elif error[0] == '(':
            error_tuple = ast.literal_eval(error)
            err_prefix = error_tuple[1]
        else:
            prefix = re.split(regexPattern, error)
            prefix = list(filter(lambda s: any([c.isalnum() for c in s]), prefix))[0]
            err_prefix = re.sub(r'([\'"{}\\><*])', '', prefix).replace("(", ' ').replace("[", '').replace("]",'').strip()

        # Update error dictionary for error and append to logs
        errlog_dictionary["error"] = error
        errlog_dictionary["err_prefix"] = err_prefix
        category = error_categories_EE2.add_category(errlog_dictionary)
        errlog_dictionary["category"] = category

    else:
        # Error can be empty tuple
        if len(error) == 2:
            errlog_dictionary["error"] = "_NULL_"
            errlog_dictionary["err_prefix"] = "_NULL_"
            errlog_dictionary["category"] = "_NULL_"
        elif 'No such file or directory' in error:
            error = error[1:-1].strip()
            err_prefix = "No such file or directory"
        else:
            prefix = re.split(regexPattern, error)
            prefix = list(filter(lambda s: any([c.isalnum() for c in s]), prefix))[0]
            err_prefix = re.sub(r'([\'"{}\\><*])', '', prefix).replace("(", ' ').replace("[", '').replace("]",'').strip()
            # Update error dictionary for error and append to logs
            errlog_dictionary["error"] = error
            errlog_dictionary["err_prefix"] = err_prefix
            category = error_categories_EE2.add_category(errlog_dictionary)
            errlog_dictionary["category"] = category
    return errlog_dictionary
