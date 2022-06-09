class HipInformation:
    # Class storing information about predictions on a canine hip regarding the hip dysplasia grade for each hip
    def __init__(self, left_acetabular, left_femoral, right_femoral, right_acetabular, model):
        self.left_acetabular = left_acetabular
        self.left_femoral = left_femoral
        self.right_femoral = right_femoral
        self.right_acetabular = right_acetabular
        self.left_hip_angle = 0
        self.right_hip_angle = 0
        self.left_hip_class = ""
        self.right_hip_class = ""
        self.model = model
        self.file_name = ""
