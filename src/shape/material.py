class Material:
    def __init__(self, name="default", reflection=0, refraction=0, refractive_index = 1):
        if reflection > 0 and refraction > 0:
            print("Reflection and refraction can not be occur at the same time.")
        if reflection > 1 or refraction > 1:
            print("Reflection or refraction can not be bigger than one.")
        self.name = name
        self.reflection = reflection
        self.refraction = refraction
        self.refractive_index = refractive_index
        self.diffuse = 1
        if reflection > 0:
            self.diffuse = 1 - reflection
        elif refraction > 0:
            self.diffuse = 1 - refraction

    def shouldBounce(self) -> bool:
        return self.reflection > 0 or self.refraction > 0

    def shouldReflect(self) -> bool:
        return self.reflection > 0