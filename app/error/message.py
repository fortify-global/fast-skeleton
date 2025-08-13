"""
Each exceptions has their error dict.
"""
"""
App error messages
"""
am = {
    'default': 'App related error occured',
    'invalid_credentials': 'Incorrect credentials',
    'exceed_quota': 'You have used all your quota limit',
    'unhandled_exception':'Not currently handled, for more information please check reason or detail if available'
}

"""
Database error messages
"""

dm = {
    'default': 'Datbase releated error occured',
    'connection_error': 'Unable to connect to databse. Check reason or detail',
    'query_error': 'We are not able to execute the query. Check reason or detail'
}

"""
Third party error messages
"""
tm = {

}