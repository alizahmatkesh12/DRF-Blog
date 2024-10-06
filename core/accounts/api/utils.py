import threading


class EmailThread(threading.Thread):
    # overriding constructor
    def __init__(self, email_obj):
        # calling parent class constructor
        self.email_obj = email_obj
        threading.Thread.__init__(self)


    # overriding run method
    def run(self):
        self.email_obj.send()
        
# class EmailThread(threading.Thread):
#     def __init__(self, email_obj):
#         self.email_obj = email_obj
#         threading.Thread.__init__(self)

#     def run(self):
#         self.email_obj.send(fail_silently=False)
