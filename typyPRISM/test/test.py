

if __name__ == '__main__':
    import unittest 

    suite = unittest.TestLoader().discover('.', pattern = "*_TestCase.py")
    unittest.TextTestRunner(verbosity=2).run(suite)
