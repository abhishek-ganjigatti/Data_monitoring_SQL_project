import cv2
from pyzbar import pyzbar
import datetime
import mysql.connector

# Connect to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abhi",
    database="project1"
)

cursor = db.cursor()

def scan_barcode():
    # Open the camera
    cap = cv2.VideoCapture(0)

    # Initialize the flag to track whether a barcode has already been processed
    barcode_processed = False

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Find barcodes in the frame
        barcodes = pyzbar.decode(frame)

        # Loop over the detected barcodes
        for barcode in barcodes:
            # Extract the bounding box location of the barcode
            (x, y, w, h) = barcode.rect

            # Draw a rectangle around the barcode
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Convert the barcode data to a string
            barcode_data = barcode.data.decode("utf-8")
            
            # Get the current date and time
            now = datetime.datetime.now()

            # Check if the barcode has already been processed
            if not barcode_processed:
                # Insert the barcode data, student ID, date, and time into the database
                sql = "INSERT INTO students (name, student_id, date, time) VALUES (%s, %s, %s, %s)"
                val = (barcode_data, 12345, now.date(), now.time())
                cursor.execute(sql, val)

                # Commit the changes
                db.commit()

                # Print the barcode data, date, and time
                print(f"Barcode Data: {barcode_data}")
                print(f"Scan Date: {now.date()}, Scan Time: {now.time()}")

                # Set the flag to indicate that the barcode has been processed
                barcode_processed = True

        # Show the frame with the detected barcodes
        cv2.imshow("Barcode Scanner", frame)

        # Check for the 'q' key to quit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Reset the flag after a delay
        if barcode_processed:
            cv2.waitKey(3500)
            barcode_processed = False

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_barcode()
