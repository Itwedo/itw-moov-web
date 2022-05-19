from PIL import Image

sample = {
    "c9a582c2c2c52ce6f8034b54d793b89f360ddf72_0.jpg": "768x512",
    "75ca6aea9a4c5fa29ab73f35faea34c9518e7678.jpg": "768x465",
    "feb0a2eb4003e0826c72a27e83f52e6f18e1b35d_0.jpg": "768x512",
    "32d1db633f1ff8f40fc3a85488ca4f21e948fc15_3.jpg": "768x512",
    "ac7122186b70128ba7d36b183d82546c27bd9771.jpg": "768x511",
    "3995a74152e86dc5c94b3debc8354b7af2166471.jpg": "768x512",
    "119f3535747e795e23ee9a1742a4b231e22b497a_9.jpg": "768x512",
    "1356c3accde1ba914c1bdeb3e62f479f64690223_6.jpg": "768x479",
    "c249c71a830c5e2eeacc1275d2c724b8ee29b97f_3.jpg": "768x512",
    "ec2553cf751608f2bd1e852b7f0bcc65764d53e8_10.jpg": "768x512",
    "elgeco_0.jpg": "640x360",
    "K25-CENI.jpg": "644x362",
}
sample_filter = {
    "TOKOjpeg.jpg": "300x225",
    "mada_day_tokyo.jpg": "245x127",
    "050717_nikki_haley_us_north_korea.jpg": "147x111",
    "05072017-tour-de-france-aru-afp-m.jpg": "147x111",
    "VAOVAO_170.png": "247x164",
    "VAOVAO_175.png": "247x164",
    "madagascar2.jpg": "640x416",
}


# def test_sample():
#     sample_ok = 0
#     sample_not = 0
#     for filename, value in sample.items():
#         with open(
#             f"/Users/mampionona/projects/telma/moov/MOOV.MG/moov/sites/default/files/{filename}",
#             "rb",
#         ) as f:
#             _size = Image.open(
#                 f"/Users/mampionona/projects/telma/moov/MOOV.MG/moov/sites/default/files/{filename}"
#             ).size
#             if _size[1] < 600:
#                 sample_not += 1
#             else:
#                 sample_ok += 1
#     expected = len(sample)
#     assert expected == sample_ok and sample_not == 0


# def test_sample_filter():
#     sample_filter_ok = 0
#     sample_filter_not = 0
#     for filename, value in sample_filter.items():
#         with open(
#             f"/Users/mampionona/projects/telma/moov/MOOV.MG/moov/sites/default/files/{filename}",
#             "rb",
#         ) as f:
#             width = Image.open(
#                 f"/Users/mampionona/projects/telma/moov/MOOV.MG/moov/sites/default/files/{filename}"
#             ).width
#             if width < 600:
#                 sample_filter_not += 1
#             else:
#                 sample_filter_ok += 1
#     expected = len(sample_filter)
#     assert expected == sample_filter_not and sample_filter_ok == 0


def test_size():
    for filename, value in sample_filter.items():
        with open(
            f"/Users/mampionona/projects/telma/moov/MOOV.MG/moov/sites/default/files/{filename}",
            "rb",
        ) as f:
            image = Image.open(
                f"/Users/mampionona/projects/telma/moov/MOOV.MG/moov/sites/default/files/{filename}"
            )
            sizes = value.split("x")
            print(sizes)
            assert (
                int(sizes[0]) == image.width and int(sizes[1]) == image.height
            )
    for filename, value in sample.items():
        with open(
            f"/Users/mampionona/projects/telma/moov/MOOV.MG/moov/sites/default/files/{filename}",
            "rb",
        ) as f:
            image = Image.open(
                f"/Users/mampionona/projects/telma/moov/MOOV.MG/moov/sites/default/files/{filename}"
            )
            sizes = value.split("x")
            print(sizes)
            assert (
                int(sizes[0]) == image.width and int(sizes[1]) == image.height
            )
