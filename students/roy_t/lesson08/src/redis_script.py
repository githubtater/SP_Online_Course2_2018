"""
    demonstrate use of Redis
"""


import login_database
import utilities


def run_example():
    """
        uses non-presistent Redis only (as a cache)

    """

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        log.info('Step 2: cache some data in Redis')
        r.set('andy', 'andy@somewhere.com')

        log.info('Step 2: now I can read it')
        email = r.get('andy')
        log.info('But I must know the key')
        log.info(f'The results of r.get: {email}')

        log.info('Step 3: cache more data in Redis')
        r.set('pam', 'pam@anywhere.com')
        r.set('fred', 'fred@fearless.com')

        log.info('Step 4: delete from cache')
        r.delete('andy')
        log.info(f'r.delete means andy is now: {email}')

        log.info(
            'Step 6: Redis can maintain a unique ID or count very efficiently')
        r.set('user_count', 21)
        r.incr('user_count')
        r.incr('user_count')
        r.decr('user_count')
        result = r.get('user_count')
        log.info('I could use this to generate unique ids')
        log.info(f'Redis says 21+1+1-1={result}')

        log.info('Step 7: richer data for a SKU')
        r.rpush('186675', 'chair')
        r.rpush('186675', 'red')
        r.rpush('186675', 'leather')
        r.rpush('186675', '5.99')

        log.info('Step 8: pull some data from the structure')
        cover_type = r.lindex('186675', 2)
        log.info(f'Type of cover = {cover_type}')


        log.info('Step 9: store customer data')
        r.rpush('Andy Dwyer', '456-555-7946')
        r.rpush('Andy Dwyer', '97456')
        r.rpush('Leslie Knope', '456-555-9654')
        r.rpush('Leslie Knope', '97453')
        r.rpush('Ron Swanson', 'Unknown')
        r.rpush('Ron Swanson', 'Unknown')
        r.rpush('Chris Trager', '456-555-9874')
        r.rpush('Chris Trager', '97453')
        r.rpush('Tom Havaford', '456-555-3214')
        r.rpush('Tom Havaford', '97456')
        r.rpush('Donna Smigle', '456-555-6544')
        r.rpush('Donna Smigle', '97456')

        log.info('Step 10: pull some customer data from the structure')
        customer_names = ['Andy Dwyer', 'Leslie Knope', 'Ron Swanson',
                            'Chris Trager', 'Tom Havaford', 'Donna Smigle']
        for customer in customer_names:
            phone = r.lindex(customer, 0)
            zipcode = r.lindex(customer, 1)
            log.info(f'Customer {customer} is located in {zipcode} and can be reached at {phone}')


    except Exception as e:
        print(f'Redis error: {e}')
