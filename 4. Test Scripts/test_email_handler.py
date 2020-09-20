import sys
sys.path.append('../')

import EmailHandler

def test_send_mail():
    test_handler = EmailHandler.EmailHandler.get_email_handler()
    assert test_handler.send_email('nimal.bandara363@gmail.com', '98741236o', {'to': 'isuruboyagane15@gmail.com,isuruboyagane.16@cse.mrt.ac.lk',
                                                                               'cc' :'dilum.xeon@gmail.com',
                                                                               'bcc': '',
                                                                               'subject':"test subject",
                                                                               'content':'test content1',
                                                                               'closure':'test closure',
                                                                               'attachments':[]
                                                                               }, 'nimal') == True

    assert test_handler.send_email('nimal.bandara363@gmail.com', '98741236o',
                                   {'to': '',
                                    'cc': 'dilum.xeon@gmail.com',
                                    'bcc': '',
                                    'subject': "test subject",
                                    'content': 'test content1',
                                    'closure': 'test closure',
                                    'attachments': []
                                    }, 'nimal') == True

    assert test_handler.send_email('nimal.bandara363@gmail.com', '98741236o',
                                   {'to': '',
                                    'cc': '',
                                    'bcc': '',
                                    'subject': "test subject",
                                    'content': 'test content1',
                                    'closure': 'test closure',
                                    'attachments': []
                                    }, 'nimal') == False


def test_verify_user():
    test_handler = EmailHandler.EmailHandler.get_email_handler()
    assert test_handler.verify_user('kjdhfajkdhk', 'kjdhfkak') == False
    assert test_handler.verify_user('', 'kjdhfkak') == None
    assert test_handler.verify_user('kjdhfajkdhk', '') == False
    assert test_handler.verify_user('', '') == None
    #run without internet
    # assert test_handler.verify_user('nimal.bandara363@gmail.com', '98741236o') == None

# def test_load_email():
