class Material:
    def __init__(self, name="default",reflection=0, refraction=0):
        if reflection > 0 and refraction > 0:
            print("Reflection and refraction can not be occur at the same time.")
        if reflection > 1 or refraction > 1:
            print("Reflection or refraction can not be bigger than one.")
        self.name = name
        self.reflection = reflection
        self.refraction = refraction
        self.diffuse = 1 - reflection if reflection > 0 else 1 - refraction
