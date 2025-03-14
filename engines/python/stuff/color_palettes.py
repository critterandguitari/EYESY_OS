import random

abcd_palettes = [
    {
        "name": "Original",
        "a": [0.500, 0.500, 0.500],
        "b": [0.500, 0.500, 0.500],
        "c": [0.500, 0.500, 0.500],
        "d": [0.500, 0.500, 0.500],
    },
    {
        "name": "Greyscale",
        "a": [0.500, 0.500, 0.500],
        "b": [0.500, 0.500, 0.500],
        "c": [0.500, 0.500, 0.500],
        "d": [0.500, 0.500, 0.500],
    },
    {
        "name": "Red : White",
        "a": [0.500, 0.500, 0.500],
        "b": [0.500, 0.500, 0.500],
        "c": [0.000, 0.450, 0.450],
        "d": [0.000, 0.530, 0.530],
    },
    {
        "name": "Black : Red",
        "a": [0.500, 0.500, 0.500],
        "b": [0.500, 0.500, -0.500],
        "c": [0.500, 0.000, 0.000],
        "d": [0.500, 0.500, 0.000],
    },
    {
        "name": "Orange : White",
        "a": [1.000, 0.500, 0.500],
        "b": [0.500, 0.500, 0.500],
        "c": [0.000, 0.250, 0.490],
        "d": [0.000, -1.267, -0.503],
    },
    {
        "name": "Black : Orange",
        "a": [0.500, 0.500, 0.500],
        "b": [0.500, 0.500, 0.500],
        "c": [0.450, 0.250, 0.000],
        "d": [-0.490, 0.503, 0.500],
    },
    {
        "name": "Yellow : White",
        "a": [0.500, 0.500, 0.500],
        "b": [0.500, 0.500, 0.500],
        "c": [0.000, 0.000, 0.500],
        "d": [0.000, 0.000, 0.500],
    },
    {
        "name": "Black : Yellow",
        "a": [0.500, 0.500, 0.500],
        "b": [0.500, 0.500, -0.500],
        "c": [0.500, 0.500, 0.000],
        "d": [0.500, 0.500, 0.000],
    },
    {
        "name": "Green : White",
        "a": [0.500, 0.500, 0.500],
        "b": [0.500, 0.500, 0.500],
        "c": [0.500, 0.000, 0.500],
        "d": [0.500, 0.000, 0.500],
    },
    {
        "name": "Black : Green",
        "a": [0.500, 0.500, 0.500],
        "b": [0.500, 0.500, -0.500],
        "c": [0.000, 0.500, 0.000],
        "d": [0.500, 0.500, 0.000],
    },
    {
        "name": "Light Blue : White",
        "a": [0.500, 0.500, 0.500],
        "b": [0.500, 0.500, 0.500],
        "c": [0.500, 0.000, 0.000],
        "d": [-0.500, 0.000, 0.000],
    },
    {
        "name": "Black : Light Blue",
        "a": [0.500, 0.500, 0.500],
        "b": [0.500, 0.500, 0.500],
        "c": [0.000, 0.500, 0.500],
        "d": [0.500, 0.500, 0.500],
    },
    {
        "name": "Blue : White",
        "a": [0.500, 0.500, 0.500],
        "b": [0.500, 0.500, 0.500],
        "c": [0.450, 0.450, 0.000],
        "d": [0.530, 0.533, 0.000],
    },
    {
        "name": "Black : Blue",
        "a": [0.500, 0.500, 0.500],
        "b": [0.500, 0.500, -0.500],
        "c": [0.000, 0.000, 0.500],
        "d": [0.500, 0.500, 0.000],
    },
    {
        "name": "Purple : White",
        "a": [0.500, 0.500, 0.500],
        "b": [0.500, 0.500, 0.500],
        "c": [0.300, 0.460, 0.000],
        "d": [0.700, 0.523, 0.000],
    },
    {
        "name": "Black : Purple",
        "a": [0.500, -0.620, 0.500],
        "b": [0.500, 0.500, 0.500],
        "c": [0.200, 0.000, 0.500],
        "d": [-0.500, 0.000, -0.493],
    },
    {
        "name": "Pink : White",
        "a": [0.498, 0.490, 0.498],
        "b": [0.498, 0.498, 0.498],
        "c": [0.000, -0.500, 0.000],
        "d": [-0.003, 0.503, -0.002],
    },
    {
        "name": "Black : Pink",
        "a": [0.500, 0.500, 0.500],
        "b": [0.500, 0.500, -0.500],
        "c": [0.500, 0.000, 0.500],
        "d": [0.500, 0.500, 0.000],
    },
    {
        "name": "Dark Blue : Light Blue",
        "a": [0.500, 0.500, 0.500],
        "b": [0.498, 0.498, -0.500],
        "c": [0.000, 0.500, 0.000],
        "d": [0.500, 0.500, 0.500],
    },
    {
        "name": "Classic Anaglyph",
        "a": [0.000, 0.000, 0.000],
        "b": [1.000, 1.000, 1.000],
        "c": [0.300, 0.250, 0.250],
        "d": [0.870, 0.755, 0.755],
    },
    {
        "name": "Red : Teal : White",
        "a": [0.500, 0.500, 0.500],
        "b": [0.500, 0.500, 0.500],
        "c": [1.000, 0.500, 0.500],
        "d": [0.000, -0.517, -0.517],
    },
    {
        "name": "Purple : Teal : Ivory",
        "a": [1.710, 0.500, 0.918],
        "b": [-1.392, 0.510, 0.720],
        "c": [-0.249, 0.359, 0.127],
        "d": [0.088, -0.403, 2.617],
    },
    {
        "name": "Deep Myrtle : Electric Purple",
        "a": [0.000, -0.050, 0.000],
        "b": [0.780, 0.630, 1.000],
        "c": [0.300, 0.588, 0.250],
        "d": [0.730, -0.247, 0.755],
    },
    {
        "name": "Pansy",
        "a": [0.000, 0.000, 0.000],
        "b": [1.000, 1.000, 1.000],
        "c": [0.250, 0.250, 0.500],
        "d": [0.737, 0.737, 0.737],
    },
    {
        "name": "Raw Sienna : Cyan",
        "a": [0.000, 0.288, 0.000],
        "b": [1.000, 1.000, 1.000],
        "c": [0.300, 0.250, 0.250],
        "d": [0.870, 0.755, 0.755],
    },
    {
        "name": "Watermelon",
        "a": [2.158, 0.590, 0.918],
        "b": [-1.392, 0.510, 0.720],
        "c": [-0.240, 0.800, 0.127],
        "d": [0.088, -0.362, 2.617],
    },
    {
        "name": "Amaranth Purple : Ivory",
        "a": [1.710, 0.500, 0.918],
        "b": [-1.080, 0.510, 0.720],
        "c": [-0.249, 0.359, 0.127],
        "d": [0.088, -0.403, 2.617],
    },
    {
        "name": "Amethyst : Malachite",
        "a": [0.510, 0.510, 0.510],
        "b": [0.291, 0.291, 0.291],
        "c": [1.000, -0.770, 0.230],
        "d": [-0.190, -0.247, -0.153],
    },
    {
        "name": "Neon Green : Citrine",
        "a": [0.500, 0.740, -1.810],
        "b": [0.450, 0.190, 2.210],
        "c": [-0.310, 0.898, 0.210],
        "d": [-0.632, -0.957, 1.998],
    },
    {
        "name": "Apricot : Electric Purple",
        "a": [0.500, 0.280, 0.608],
        "b": [0.500, 0.500, 0.500],
        "c": [0.250, 1.520, 0.250],
        "d": [0.000, 0.000, -0.312],
    },
    {
        "name": "Baja",
        "a": [0.498, -0.470, -0.680],
        "b": [0.468, 1.028, 1.620],
        "c": [-1.150, 0.718, 0.450],
        "d": [-0.252, -0.487, 1.817],
    },
    {
        "name": "Abajo",
        "a": [0.498, -0.390, -0.680],
        "b": [0.468, 1.028, 1.620],
        "c": [-1.150, 0.558, 0.450],
        "d": [-0.252, -0.487, 1.817],
    },
    {
        "name": "Aquamarine : Light Purple",
        "a": [0.340, 0.530, 0.518],
        "b": [-0.240, -0.450, -0.150],
        "c": [-1.552, 0.718, 0.850],
        "d": [0.088, -0.507, 4.557],
    },
    {
        "name": "Looking West",
        "a": [0.530, 0.698, -0.640],
        "b": [0.450, 0.210, 1.620],
        "c": [-0.310, 1.840, 0.210],
        "d": [-0.670, -0.742, 1.998],
    },
    {
        "name": "Looking West Evening",
        "a": [0.490, 0.358, -1.642],
        "b": [0.450, 0.190, 2.210],
        "c": [-0.310, 1.840, 0.210],
        "d": [-0.632, -0.957, 1.998],
    },
    {
        "name": "2090s",
        "a": [1.068, 0.648, 0.718],
        "b": [-1.212, -0.362, 0.068],
        "c": [-0.562, 0.878, 0.280],
        "d": [0.538, -0.527, -0.382],
    },
    {
        "name": "Highlights",
        "a": [0.500, 0.500, 0.500],
        "b": [0.500, 0.500, 0.500],
        "c": [1.000, 0.500, 0.500],
        "d": [0.000, 0.000, -0.523],
    },
    {
        "name": "Perfume",
        "a": [1.098, 1.170, 0.648],
        "b": [0.500, -0.272, 1.568],
        "c": [-0.492, 0.900, 0.280],
        "d": [-1.250, 0.193, 0.628],
    },
    {
        "name": "Gymnopedie No. 3",
        "a": [0.500, 0.530, 0.680],
        "b": [0.498, 0.498, 0.250],
        "c": [0.840, 1.700, 3.440],
        "d": [0.120, 0.583, 0.498],
    },
    {
        "name": "Almost Rainbow",
        "a": [1.400, 0.590, 0.770],
        "b": [-1.392, 0.640, 0.720],
        "c": [-1.220, 1.070, 0.127],
        "d": [0.088, -0.362, 2.617],
    },
    {
        "name": "KRYCB",
        "a": [-0.212, -0.470, -0.682],
        "b": [3.138, 3.138, 3.138],
        "c": [-0.790, 0.718, 0.428],
        "d": [-0.672, -0.422, 4.557],
    },
    {
        "name": "Discrete Variety!",
        "a": [0.000, 0.000, 0.000],
        "b": [1.000, 1.000, 1.000],
        "c": [250.000, 251.000, 252.000],
        "d": [0.000, 0.683, 0.000],
    },
    {
        "name": "Palette 1",
        "a": [0.332, 0.347, 0.404],
        "b": [0.944, 0.346, 0.315],
        "c": [0.368, 0.980, 1.422],
        "d": [4.571, 2.412, 4.308],
    }
]

