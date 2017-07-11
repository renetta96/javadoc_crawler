class Version:
    JAVA6 = '1.6'
    JAVA7 = '1.7'
    JAVA8 = '1.8'

    @classmethod
    def get_list(cls):
        return cls.JAVA6, cls.JAVA7, cls.JAVA8
