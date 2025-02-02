import json
import pdfkit
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def replace_dots_in_keys(data):
    if isinstance(data, dict):
        return {key.replace(".", "_"): replace_dots_in_keys(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [replace_dots_in_keys(item) for item in data]
    else:
        return data
    
    
@csrf_exempt
def submit_form(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Load the JSON data from the request
            data = replace_dots_in_keys(data)  # Replace dots with underscores
            print(data)  # Now all keys have underscores instead of dots

            # Load and render the HTML template dynamically with data
            html_content = render_to_string("email-templates/email.html", {"data": data})

            # Save the rendered HTML content to a file
            html_file_path = "form.html"
            with open(html_file_path, "w", encoding="utf-8") as file:
                file.write(html_content)

            # Convert the HTML file to a PDF
            pdf_file_path = "form.pdf"
            pdfkit.from_file(html_file_path, pdf_file_path)

            # Email configuration
            subject = "New Form Submission"
            recipient_email = "sameer.akbar@alnafi.com"  # Change this

            # Create email with attachment
            email = EmailMessage(
                subject,
                "Please find the attached form submission PDF.",
                "muhammadsameer.css@gmail.com",  # Replace with your email
                [recipient_email],
            )

            # Attach the generated PDF
            with open(pdf_file_path, "rb") as pdf_file:
                email.attach("form.pdf", pdf_file.read(), "application/pdf")

            # Send the email
            email.send()

            return JsonResponse({"message": "Form received, PDF generated, and email sent!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
