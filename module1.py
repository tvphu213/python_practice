class Module1:
    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.list_odd_numbers = Module1.create_list_odd_numbers(min, max)
        self.list_multiple_of_three = Module1.create_list_multiple_of_three(min, max)

    @staticmethod
    def create_list_odd_numbers(min, max):
        """
        Ham tra ve list so le trong range
        """
        return [number for number in range(min, max) if number % 2 == 1]

    @staticmethod
    def create_list_multiple_of_three(min, max):
        """
        Ham tra ve list so chia het cho 3 trong range
        """
        return [number for number in range(min, max) if number % 3 == 0]

    @staticmethod
    def intersect_2_list(list1, list2):
        return list(set(list1).intersection(list2))

