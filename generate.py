
from PIL import Image
import random
import os
import uuid
from datetime import datetime

def generate(source_file_dir, size_x=10, size_y=10, max_squares=12, 
    square_dimension=105, save=True, output_dir="output", display=False):

    square_size = (square_dimension, square_dimension)
    quilt_size = (size_x * square_dimension, size_y * square_dimension)
    quilt = Image.new('RGB', quilt_size)

    images = []
    for file_name in os.listdir(source_file_dir):
        f = Image.open(os.path.join(source_file_dir, file_name))
        f.thumbnail(square_size)

        images.append(f)

    image_counts = {}
    available_images = range(0, len(images))
    for i in range(0, size_x):
        for j in range(0, size_y):
            while True:
                image_index_number = random.randint(0, len(available_images)-1)
                image_number = available_images[image_index_number]
                image_count = image_counts.get(image_number, 0)
                if image_count < max_squares:
                    image_counts[image_number] = image_count + 1
                    quilt.paste(
                        images[image_number], 
                        (i*square_dimension, j*square_dimension)
                    )
                    break
                else:
                    available_images.remove(image_number)

    if save:
        quilt.save("{}/{}.jpg".format(output_dir, datetime.now()), "jpeg")

    if display:
        quilt.show()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source", 
        help="Directory where source images are located."
    )
    parser.add_argument(
        "--repetitions", type=int, default=1, 
        help="The number of images to generate."
    )
    parser.add_argument(
        "--width", type=int, default=10, 
        help="The number of squares to have width-wise."
    )
    parser.add_argument(
        "--height", type=int, default=10,
        help="The number of squares to have height-wise."
    )
    parser.add_argument(
        "--max", type=int, default=12,
        help="The maximum number of each image to include."
    )
    parser.add_argument(
        "--square_width", type=int, default=105,
        help="The length of a side of an individual square."
    )
    parser.add_argument(
        "--save", type=bool, default=True,
        help="Whether to save the image to a file."
    )
    parser.add_argument(
        "--output", default="output",
        help="Directory where to generated images are saved."
    )
    parser.add_argument(
        "--display", type=bool, default=False,
        help="Whether to display the image."
    )
    args = parser.parse_args()

    if args.save:
        if not os.path.exists(args.output):
            os.makedirs(args.output)

    for i in range(0, args.repetitions):
        generate(
            args.source, 
            size_x=args.width, 
            size_y=args.height, 
            max_squares=args.max, 
            square_dimension=args.square_width, 
            save=args.save, 
            output_dir=args.output, 
            display=args.display
        )
    