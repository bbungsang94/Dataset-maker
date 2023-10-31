def get_coordinates():
    # Global 좌표
    standing = [
        [-0.000003, 0.025424, 0.441971],  # 머리마루점(Occipital bone)
        [-0.046556, -0.068851, 0.328275],  # 눈초리점(Eye Socket, 우)
        [0.046712, -0.06869, 0.328387],  # 눈초리점(Eye Socket, 좌)
        [-0.076753, 0.002704, 0.309184],  # 귀구슬점(Earlobe, 우)
        [0.076753, 0.002704, 0.309184],  # 귀구슬점(Earlobe, 좌)
        [-0.077523, 0.00283, 0.320535],  # 귀바퀴위뿌리점(Tragus, 우)
        [0.077523, 0.00283, 0.320535],  # 귀바퀴위뿌리점(Tragus, 좌)
        [0.000073, -0.092186, 0.351445],  # 눈살점(Glabella)
        [0.000269, -0.093741, 0.337248],  # 코뿌리점(Sellion)
        [0.000015, -0.090321, 0.210503],  # 턱끝점(Menton)
        [-0.000003, 0.116093, 0.352571],  # 뒤통수 돌출점(Occiput)
        [-0.000003, 0.07858, 0.251812],  # 뒤통수점(Inion)
        [-0.068402, -0.03547, 0.347917],  # 머리옆점(Euryon, 우)
        [0.068958, -0.034751, 0.348294],  # 머리옆점(Euryon, 좌)
        [-0.03405, -0.077515, 0.322053],  # 눈확아래점(Inferior Orbitale, 우)
        [0.033958, -0.077413, 0.322128],  # 눈확아래점(Inferior Orbitale, 좌)
        [0.000004, 0.097569, 0.157897],  # 목뒤점(Cervicale)
        [0.000005, -0.030337, 0.12267],  # 목앞점(Anterior Neck)
        [-0.060985, 0.007459, 0.180173],  # 목옆점(Lateral Neck, 우)
        [0.061099, 0.007635, 0.180319],  # 목옆점(Lateral Neck, 좌)
        [-0.000006, -0.046593, 0.177639],  # 방패연골아래점(Inferior Thyroid)
        [-0.179889, 0.024175, 0.151491],  # 어깨점(Acromion, 우)
        [0.179892, 0.024178, 0.151493],  # 어깨점(Acromion, 좌)
        [-0.118015, 0.038155, 0.154849],  # 어깨가쪽점(Lateral Shoulder, 우)
        [0.118019, 0.03816, 0.15485],  # 어깨가쪽점(Lateral Shoulder, 좌)
        [-0.221789, 0.028579, -0.003102],  # 겨드랑이점(Axilla, 우)
        [0.221788, 0.028579, -0.003101],  # 겨드랑이점(Axilla, 좌)
        [-0.207827, -0.004973, 0.017877],  # 겨드랑앞점(Anterior Axilla, 우)
        [0.207826, -0.004974, 0.01788],  # 겨드랑앞점(Anterior Axilla, 좌)
        [-0.222151, 0.082484, -0.004028],  # 겨드랑뒤점(Posterior Axilla, 우)
        [0.222146, 0.082482, -0.004028],  # 겨드랑뒤점(Posterior Axilla, 좌)
        [-0.173052, -0.030637, 0.091265],  # 겨드랑앞벽점(Anterior MidAxilla, 우)
        [0.173054, -0.030636, 0.09127],  # 겨드랑앞벽점(Anterior MidAxilla, 좌)
        [-0.14755, 0.116413, 0.098559],  # 겨드랑뒤벽점(Posterior MidAxilla, 우)
        [0.147547, 0.116415, 0.098557],  # 겨드랑뒤벽점(Posterior MidAxilla, 좌)
        [0.000003, 0.124056, 0.064129],  # 등뼈위겨드랑수준점(Axillary Level at Midspine)
        [-0.199998, -0.030044, 0.035669],  # 겨드랑앞접힘점(Anterior Axillary Fold, 우)
        [0.199999, -0.030045, 0.035673],  # 겨드랑앞접힘점(Anterior Axillary Fold, 좌)
        [-0.222151, 0.082484, -0.004028],  # 겨드랑뒤점(Posterior Axilla, 우)
        [0.222146, 0.082482, -0.004028],  # 겨드랑뒤점(Posterior Axilla, 좌)
        [0.000004, -0.078771, 0.032336],  # 복장뼈가운데점(Mesosternal)
        [-0.107037, -0.105581, -0.050393],  # 젖꼭지점(Nipple, 우)
        [0.107042, -0.105592, -0.050393],  # 젖꼭지점(Nipple, 좌)
        [-0.13146, -0.07267, -0.081184],  # 젖가슴아래수준(Inferior Breast level, 우)
        [0.131466, -0.07268, -0.081184],  # 젖가슴아래수준(Inferior Breast level, 좌)
        [-0.155495, -0.007942, -0.216804],  # 허리옆점(Lateral Waist, 우)
        [0.155496, -0.007948, -0.21681],  # 허리옆점(Lateral Waist, 좌)
        [0.000004, -0.132918, -0.233358],  # 허리앞점(Anterior Waist)
        [-0.000003, 0.091046, -0.236951],  # 허리뒤점(Posterior Waist)
        [-0.155495, -0.007942, -0.216804],  # 허리수준(Lateral Waist level, 우)
        [0.155496, -0.007948, -0.21681],  # 허리수준(Lateral Waist level, 좌)
        [-0.160365, -0.001689, -0.155293],  # 중간허리수준(Midriff level, 우)
        [0.160367, -0.001697, -0.155296],  # 중간허리수준(Midriff level, 좌)
        [0.000002, -0.131549, -0.256985],  # 배돌출점(Stomach tip)
        [0.000001, -0.126774, -0.290072],  # 배꼽점(Stomach navel)
        [-0.164664, 0.013356, -0.270792],  # 배꼽수준허리옆점(Lateral Waist omphalion, 우)
        [0.164664, 0.013356, -0.270792],  # 배꼽수준허리옆점(Lateral Waist omphalion, 좌)
        [-0.000003, 0.100244, -0.289525],  # 배꼽수준허리뒤점(Posterior Waist omphalion)
        [-0.061006, 0.153625, -0.415752],  # 엉덩이돌출점(Buttock Protrusion, 우)
        [0.061006, 0.153625, -0.415752],  # 엉덩이돌출점(Buttock Protrusion, 좌)
        [0.061006, 0.153625, -0.415752],  # 엉덩이돌출점수준(Buttock Protrusion level, 우)
        [0.098136, -0.088733, -0.41456],  # 엉덩이돌출점수준(Buttock Protrusion level, 좌)
        [-0.062043, 0.13964, -0.367867],  # Top-hip점(Top-hip, 우)
        [0.062042, 0.139637, -0.367867],  # Top-hip점(Top-hip, 좌)
        [-0.062043, 0.13964, -0.367867],  # Top-hip 수준(Top-hip level, 우)
        [0.096788, -0.087541, -0.365453],  # Top-hip 수준(Top-hip level, 좌)
        [-0.083322, 0.123794, -0.344732],  # Upper-hip점(Upper-hip, 우)
        [0.083322, 0.123794, -0.344732],  # Upper-hip점(Upper-hip, 좌)
        [-0.083322, 0.123794, -0.344732],  # Upper-hip 수준(Upper-hip level, 우)
        [0.09703, -0.08834, -0.344718],  # Upper-hip 수준(Upper-hip level, 좌)
        [-0.180726, 0.023082, -0.448773],  # 엉덩이최대둘레수준(Hip-width level, 우)
        [0.180726, 0.023082, -0.448773],  # 엉덩이최대둘레수준(Hip-width level, 좌)
        [-0.090556, 0.113142, -0.540854],  # 볼기고랑점(Gluteal Fold, 우)
        [0.090556, 0.113142, -0.540854],  # 볼기고랑점(Gluteal Fold, 좌)
        [-0.000001, -0.033277, -0.555264],  # 샅점(Crotch)
        [-0.09652, -0.04576, -0.868488],  # 무릎뼈위점(Superior Patella, 우)
        [0.09652, -0.04576, -0.868488],  # 무릎뼈위점(Superior Patella, 좌)
        [-0.095054, -0.036428, -0.893663],  # 무릎뼈가운데점(Midpatella, 우)
        [0.095054, -0.036428, -0.893663],  # 무릎뼈가운데점(Midpatella, 좌)
        [-0.095372, -0.023985, -0.916178],  # 무릎뼈아래점(Inferior Patella, 우)
        [0.095372, -0.023985, -0.916178],  # 무릎뼈아래점(Inferior Patella, 좌)
        [-0.18718, 0.0109, -0.527117],  # 넙적다리가운데점(Midthigh, 우)
        [0.18718, 0.0109, -0.527117],  # 넙적다리가운데점(Midthigh, 좌)
        [-0.091315, 0.08765, -0.860128],  # 오금점(Posterior Juncture of Calf and Thigh, 우)
        [0.091315, 0.08765, -0.860128],  # 오금점(Posterior Juncture of Calf and Thigh, 좌)
        [-0.106494, 0.121945, -1.02879],  # 장딴지돌출점(Calf Protrusion, 우)
        [0.106494, 0.121945, -1.02879],  # 장딴지돌출점(Calf Protrusion, 좌)
        [-0.095621, 0.023354, -1.26868],  # 종아리아래점(Inferior Leg, 우)
        [0.095621, 0.023354, -1.26868],  # 종아리아래점(Inferior Leg, 좌)
        [-0.062418, 0.04713, -1.31871],  # 안쪽복사점(Medial Malleous, 우)
        [0.062418, 0.04713, -1.31871],  # 안쪽복사점(Medial Malleous, 좌)
        [-0.128206, 0.082131, -1.31363],  # 가쪽복사점(Lateral Malleous, 우)
        [0.128206, 0.082131, -1.31363],  # 가쪽복사점(Medial Malleous, 좌)
        [-0.794376, 0.067816, 0.022871],  # 손바닥중앙점(Hand center, 우)
        [0.794374, 0.067817, 0.022872],  # 손바닥중앙점(Hand center, 좌)
        [-0.113462, -0.021057, -1.38951],  # 발바닥중앙점(Foot center, 우)
        [0.113457, -0.021056, -1.38951],  # 발바닥중앙점(Foot center, 좌)
        [-0.464522, 0.097318, 0.057199],  # 팔꿈치아래점(Bottom olecranon, 우)
        [0.464522, 0.097316, 0.057198],  # 팔꿈치아래점(Bottom olecranon, 좌)
        [-0.715033, 0.093531, 0.048505],  # 손목안쪽점(Ulnar Styloid, 우)
        [0.715033, 0.093531, 0.048505],  # 손목안쪽점(Ulnar Styloid, 좌)
        [-0.340382, 0.004545, 0.063565],  # 두갈래근점(Biceps, 우)
        [0.340382, 0.004545, 0.063565],  # 두갈래근점(Biceps, 좌)
    ]
    sitting = [
        [-0.105341, -0.090454, -0.624696],  # 앉은넙다리위점(Superior Thigh, Sitting, 우)
        [0.105341, -0.090454, -0.624696],  # 앉은넙다리위점(Superior Thigh, Sitting, 좌)
        [-0.09652, -0.04576, -0.868488],  # 앉은무릎뼈위점(Superior Patella, Sitting, 우)
        [0.09652, -0.04576, -0.868488],  # 앉은무릎뼈위점(Superior Patella, Sitting, 좌)
        [-0.095372, -0.023985, -0.916178],  # 앉은무릎앞점(Anterior Knee, Sitting, 우)
        [0.095372, -0.023985, -0.916178],  # 앉은무릎앞점(Anterior Knee, Sitting, 좌)
        [-0.091315, 0.08765, -0.860128],  # 오금점(Posterior Juncture of Calf and Thigh, 우)
        [0.091315, 0.08765, -0.860128],  # 오금점(Posterior Juncture of Calf and Thigh, 좌)
        [-0.178589, 0.010366, -0.388594],  # 앉은엉덩이최대돌출수준(Hip level, 우)
        [0.178589, 0.010366, -0.388594],  # 앉은엉덩이최대돌출수준(Hip level, 좌)
        [0.000002, -0.131549, -0.256985],  # 배돌출점(Stomach tip)
        [0.000001, 0.149724, -0.441748],  # 앉은엉덩이뒤돌출점(Gluteal Prominence)
        [-0.000003, 0.091046, -0.236951],  # 허리뒤점(Posterior Waist)
        [-0.464522, 0.097318, 0.057199],  # 팔꿈치아래점(Bottom olecranon, 우)
        [0.464522, 0.097316, 0.057198],  # 팔꿈치아래점(Bottom olecranon, 좌)
        [-0.794376, 0.067816, 0.022871],  # 손바닥중앙점(Hand center, 우)
        [0.794374, 0.067817, 0.022872],  # 손바닥중앙점(Hand center, 좌)
    ]
    return standing, sitting


def get_names():
    standing = {
        "머리마루점, Occipital bone": -1,
        "눈초리점, Eye Socket, 우": -1,
        "눈초리점, Eye Socket, 좌": -1,
        "귀구슬점, Earlobe, 우": -1,
        "귀구슬점, Earlobe, 좌": -1,
        "귀바퀴위뿌리점, Tragus, 우": -1,
        "귀바퀴위뿌리점, Tragus, 좌": -1,
        "눈살점, Glabella": -1,
        "코뿌리점, Sellion": -1,
        "턱끝점, Menton": -1,
        "뒤통수 돌출점, Occiput": -1,
        "뒤통수점, Inion": -1,
        "머리옆점, Euryon, 우": -1,
        "머리옆점, Euryon, 좌": -1,
        "눈확아래점, Inferior Orbitale, 우": -1,
        "눈확아래점, Inferior Orbitale, 좌": -1,
        "목뒤점, Cervicale": -1,
        "목앞점, Anterior Neck": -1,
        "목옆점, Lateral Neck, 우": -1,
        "목옆점, Lateral Neck, 좌": -1,
        "방패연골아래점, Inferior Thyroid": -1,
        "어깨점, Acromion, 우": -1,
        "어깨점, Acromion, 좌": -1,
        "어깨가쪽점, Lateral Shoulder, 우": -1,
        "어깨가쪽점, Lateral Shoulder, 좌": -1,
        "겨드랑이점, Axilla, 우": -1,
        "겨드랑이점, Axilla, 좌": -1,
        "겨드랑앞점, Anterior Axilla, 우": -1,
        "겨드랑앞점, Anterior Axilla, 좌": -1,
        "겨드랑뒤점, Posterior Axilla, 우": -1,
        "겨드랑뒤점, Posterior Axilla, 좌": -1,
        "겨드랑앞벽점, Anterior MidAxilla, 우": -1,
        "겨드랑앞벽점, Anterior MidAxilla, 좌": -1,
        "겨드랑뒤벽점, Posterior MidAxilla, 우": -1,
        "겨드랑뒤벽점, Posterior MidAxilla, 좌": -1,
        "등뼈위겨드랑수준점, Axillary Level at Midspine": -1,
        "겨드랑앞접힘점, Anterior Axillary Fold, 우": -1,
        "겨드랑앞접힘점, Anterior Axillary Fold, 좌": -1,
        "겨드랑뒤접힘점, Posterior Axilla Fold, 우": -1,
        "겨드랑뒤접힘점, Posterior Axilla Fold, 좌": -1,
        "복장뼈가운데점, Mesosternal": -1,
        "젖꼭지점, Nipple, 우": -1,
        "젖꼭지점, Nipple, 좌": -1,
        "젖가슴아래수준, Inferior Breast level, 우": -1,
        "젖가슴아래수준, Inferior Breast level, 좌": -1,
        "허리옆점, Lateral Waist, 우": -1,
        "허리옆점, Lateral Waist, 좌": -1,
        "허리앞점, Anterior Waist": -1,
        "허리뒤점, Posterior Waist": -1,
        "허리수준, Lateral Waist level, 우": -1,
        "허리수준, Lateral Waist level, 좌": -1,
        "중간허리수준, Midriff level, 우": -1,
        "중간허리수준, Midriff level, 좌": -1,
        "배돌출점, Stomach tip": -1,
        "배꼽점, Stomach navel": -1,
        "배꼽수준허리옆점, Lateral Waist omphalion, 우": -1,
        "배꼽수준허리옆점, Lateral Waist omphalion, 좌": -1,
        "배꼽수준허리뒤점, Posterior Waist omphalion": -1,
        "엉덩이돌출점, Buttock Protrusion, 우": -1,
        "엉덩이돌출점, Buttock Protrusion, 좌": -1,
        "엉덩이돌출점수준, Buttock Protrusion level, 우": -1,
        "엉덩이돌출점수준, Buttock Protrusion level, 좌": -1,
        "Top-hip점, Top-hip, 우": -1,
        "Top-hip점, Top-hip, 좌": -1,
        "Top-hip 수준, Top-hip level, 우": -1,
        "Top-hip 수준, Top-hip level, 좌": -1,
        "Upper-hip점, Upper-hip, 우": -1,
        "Upper-hip점, Upper-hip, 좌": -1,
        "Upper-hip 수준, Upper-hip level, 우": -1,
        "Upper-hip 수준, Upper-hip level, 좌": -1,
        "엉덩이최대둘레수준, Hip-width level, 우": -1,
        "엉덩이최대둘레수준, Hip-width level, 좌": -1,
        "볼기고랑점, Gluteal Fold, 우": -1,
        "볼기고랑점, Gluteal Fold, 좌": -1,
        "샅점, Crotch": -1,
        "무릎뼈위점, Superior Patella, 우": -1,
        "무릎뼈위점, Superior Patella, 좌": -1,
        "무릎뼈가운데점, Midpatella, 우": -1,
        "무릎뼈가운데점, Midpatella, 좌": -1,
        "무릎뼈아래점, Inferior Patella, 우": -1,
        "무릎뼈아래점, Inferior Patella, 좌": -1,
        "넙적다리가운데점, Midthigh, 우": -1,
        "넙적다리가운데점, Midthigh, 좌": -1,
        "오금점, Posterior Juncture of Calf and Thigh, 우": -1,
        "오금점, Posterior Juncture of Calf and Thigh, 좌": -1,
        "장딴지돌출점, Calf Protrusion, 우": -1,
        "장딴지돌출점, Calf Protrusion, 좌": -1,
        "종아리아래점, Inferior Leg, 우": -1,
        "종아리아래점, Inferior Leg, 좌": -1,
        "안쪽복사점, Medial Malleous, 우": -1,
        "안쪽복사점, Medial Malleous, 좌": -1,
        "가쪽복사점, Lateral Malleous, 우": -1,
        "가쪽복사점, Medial Malleous, 좌": -1,
        "손바닥중앙점, Hand center, 우": -1,
        "손바닥중앙점, Hand center, 좌": -1,
        "발바닥중앙점, Foot center, 우": -1,
        "발바닥중앙점, Foot center, 좌": -1,
        "팔꿈치아래점, Bottom olecranon, 우": -1,
        "팔꿈치아래점, Bottom olecranon, 좌": -1,
        "손목안쪽점, Ulnar Styloid, 우": -1,
        "손목안쪽점, Ulnar Styloid, 좌": -1,
        "두갈래근점, Biceps, 우": -1,
        "두갈래근점, Biceps, 좌": -1,
    }
    sitting = {
        "앉은넙다리위점, Superior Thigh, Sitting, 우": -1,
        "앉은넙다리위점, Superior Thigh, Sitting, 좌": -1,
        "앉은무릎뼈위점, Superior Patella, Sitting, 우": -1,
        "앉은무릎뼈위점, Superior Patella, Sitting, 좌": -1,
        "앉은무릎앞점, Anterior Knee, Sitting, 우": -1,
        "앉은무릎앞점, Anterior Knee, Sitting, 좌": -1,
        "오금점, Posterior Juncture of Calf and Thigh, 우": -1,
        "오금점, Posterior Juncture of Calf and Thigh, 좌": -1,
        "앉은엉덩이최대돌출수준, Hip level, 우": -1,
        "앉은엉덩이최대돌출수준, Hip level, 좌": -1,
        "배돌출점, Stomach tip": -1,
        "앉은엉덩이뒤돌출점, Gluteal Prominence": -1,
        "허리뒤점, Posterior Waist": -1,
        "팔꿈치아래점, Bottom olecranon, 우": -1,
        "팔꿈치아래점, Bottom olecranon, 좌": -1,
        "손바닥중앙점, Hand center, 우": -1,
        "손바닥중앙점, Hand center, 좌": -1,
    }
    return standing, sitting


def get_interactions():
    interactions = [
        ("머리위로뻗은주먹높이", "Overhead Fist Reach", ["Foot center, 우", "Hand center, 우"], "height", "hands-on"),
        ("키", "Stature", ["Foot center, 우", "Occipital bone"], "height", "standing"),
        ("목뒤높이", "Cervical Height", ["Foot center, 우", "Cervicale"], "height", "standing"),
        ("어깨높이", "Acromion Height", ["Foot center, 우", "Acromion, 우"], "height", "standing"),
        ("겨드랑높이", "Axilla Height", ["Foot center, 우", "Axilla, 우"], "height", "standing"),
        ("허리기준선높이", "Waist Height natural indentation", ["Foot center, 우", "Lateral Waist level, 우"], "height",
         "standing"),
        ("허리높이", "Waist Height", ["Foot center, 우", "Lateral Waist, 우"], "height", "standing"),
        ("위앞엉덩뼈가시높이", "Iliac Spine Height", ["Foot center, 우", "Top-hip, 우"], "height", "standing"),
        ("샅높이", "Crotch Height", ["Foot center, 우", "Crotch"], "height", "standing"),
        ("가쪽복사높이", "Lateral Malleolus Height", ["Foot center, 우", "Lateral Malleous, 우"], "height", "standing"),
        ("주먹높이", "Fist Height", ["Foot center, 우", "Hand center, 우"], "height", "standing"),
        ("팔꿈치높이", "Elbow Height", ["Foot center, 우", "Bottom olecranon, 우"], "height", "curve"),
        ("가슴너비", "Chest Breadth", ["Axilla, 좌", "Axilla, 우"], "width", "standing"),
        ("허리너비", "Waist Breadth", ["Lateral Waist, 좌", "Lateral Waist, 우"], "width", "standing"),
        ("엉덩이너비", "Hip Width", ["Buttock Protrusion level, 좌", "Buttock Protrusion level, 우"], "width", "standing"),
        ("발목너비", "Ankle Width", ["Inferior Leg, 좌", "Inferior Leg, 우"], "width", "standing"),
        ("겨드랑두께", "Armscye Depth", ["Posterior Axilla, 우", "Anterior Axilla, 우"], "depth", "t"),
        ("가슴두께", "Chest Depth, Standing", ["Anterior MidAxilla, 우", "Posterior MidAxilla, 우"], "depth", "t"),
        ("허리두께", "Waist Depth", ["Anterior Waist", "Posterior Waist"], "depth", "t"),
        ("목둘레", "Neck Circumference", ["Inferior Thyroid"], "circ-h", "standing"),
        ("목밑뒤길이", "Neck Circumference", ["Lateral Neck, 좌", "Cervicale", "Lateral Neck, 우"], "length", "standing"),
        ("목밑둘레", "Neck Base Circumference",
         ["Lateral Neck, 좌", "Anterior Neck", "Lateral Neck, 우", "Cervicale", "Lateral Neck, 좌"], "length", "standing"),
        ("겨드랑둘레", "Armscye Circumference",
         ["Acromion, 우", "Anterior Axilla, 우", "Axilla, 우", "Posterior Axilla, 우", "Acromion, 우"], "length",
         "standing"),
        ("편위팔둘레", "Upper Arm Circumference", ["Lateral Shoulder, 우"], "circ-v", "t"),
        ("편팔꿈치둘레", "Elbow Circumference 2", ["Bottom olecranon, 우"], "circ-v", "t"),
        ("손목둘레", "Wrist Circumference", ["Ulnar Styloid, 우"], "circ-v", "t"),
        ("위팔둘레", "Upper Arm Circumference", ["Biceps, 우"], "circ-h", "curve"),
        ("가슴둘레", "Chest Circumference", ["Anterior Axillary Fold, 우"], "circ-h", "hands-on"),
        ("젖가슴둘레", "Bust Circumference", ["Nipple, 우"], "circ-h", "hands-on"),
        ("젖가슴아래둘레", "Underbust Circumference", ["Inferior Breast level, 우"], "circ-h", "hands-on"),
        ("허리둘레", "Waist Circumference", ["Anterior Waist"], "circ-h", "hands-on"),
        ("배꼽수준허리둘레", "Omphalion Circumference", ["Stomach navel"], "circ-h", "hands-on"),
        ("엉덩이둘레", "Hip Circumference", ["Buttock Protrusion level, 우"], "circ-h", "hands-on"),
        ("넙다리둘레", "Thigh Circumference", ["Midthigh, 우"], "circ-h", "hands-on"),
        ("무릎둘레", "Knee Circumference", ["Midpatella, 우"], "circ-h", "hands-on"),
        ("종아리둘레", "Calf Circumference", ["Calf Protrusion, 우"], "circ-h", "hands-on"),
        ("목옆뒤허리둘레선길이", "Neck Point to back Waistline", ["Lateral Neck, 우", "Lateral Waist level"], "length", "t"),
        ("목옆젖꼭지길이", "Neck Shoulder Point to Nipple", ["Lateral Neck, 우", "Nipple, 우"], "length", "t"),
        ("목옆젖꼭지허리둘레선길이", "Neck Point to Breast Point to Waistline",
         ["Lateral Neck, 우", "Lateral Waist level"], "length", "t"),
        ("샅앞뒤길이", "Crotch length", ["Anterior Waist", "Crotch", "Posterior Waist"], "length", "t"),
        ("어깨목뒤길이", "Shoulder to neck(half)", ["Cervicale", "Acromion, 좌"], "length", "standing"),
        ("목뒤어깨사이길이", "Shoulder to neck(full)", ["Acromion, 우", "Cervicale", "Acromion, 좌"], "length", "standing"),
        ("위팔길이", "Upperarm Length", ["Acromion, 우", "Bottom olecranon, 우"], "width", "t"),
        ("팔길이", "Arm Length", ["Acromion, 우", "Ulnar Styloid, 우"], "width", "t"),
        ("앉은키", "Sitting Height", ["Occipital bone", "Gluteal Fold, 우"], "height", "sitting"),
        ("앉은배두께", "Sitting Height", ["Occipital bone", "Posterior Waist"], "depth", "sitting"),
        ("팔꿈치주먹수평길이", "Elbow-Grip Length", ["Hand center, 우", "Bottom olecranon, 우"], "depth", "sitting"),
    ]
    return interactions
