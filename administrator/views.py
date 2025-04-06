from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from student.models import Company, Job, JobApplication, CompanyUpload
from accounts.models import Administrator, Recruiter, Student
import json
from django.utils import timezone
import os

@login_required
def index(request):
    return render(request, "administrator/index.html")

@login_required
def manage_companies(request):
    """View for managing companies"""
    companies = Company.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(companies, 10)  # Show 10 companies per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'companies': page_obj,
        'total_companies': companies.count(),
        'active_companies': companies.filter(is_active=True).count(),
    }
    return render(request, "administrator/companies.html", context)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def company_create(request):
    """AJAX view to create a new company"""
    try:
        data = json.loads(request.body)
        company = Company.objects.create(
            name=data.get('name'),
            description=data.get('description'),
            website=data.get('website'),
            email=data.get('email'),
            location=data.get('location'),
            is_active=data.get('is_active', True)
        )
        
        return JsonResponse({
            'status': 'success',
            'company_id': company.id,
            'message': 'Company created successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["GET"])
def company_details(request, company_id):
    """AJAX view to get company details"""
    try:
        company = Company.objects.get(id=company_id)
        data = {
            'id': company.id,
            'name': company.name,
            'description': company.description,
            'website': company.website,
            'email': company.email,
            'location': company.location,
            'is_active': company.is_active,
            'logo': company.logo.url if company.logo else None,
            'created_at': company.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': company.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return JsonResponse({
            'status': 'success',
            'company': data
        })
    except Company.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Company not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def company_update(request, company_id):
    """AJAX view to update company details"""
    try:
        company = Company.objects.get(id=company_id)
        data = json.loads(request.body)
        
        company.name = data.get('name', company.name)
        company.description = data.get('description', company.description)
        company.website = data.get('website', company.website)
        company.email = data.get('email', company.email)
        company.location = data.get('location', company.location)
        company.is_active = data.get('is_active', company.is_active)
        company.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Company updated successfully!'
        })
    except Company.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Company not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def company_delete(request, company_id):
    """AJAX view to delete company"""
    try:
        company = Company.objects.get(id=company_id)
        company_name = company.name
        company.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Company "{company_name}" deleted successfully!'
        })
    except Company.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Company not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
def manage_jobs(request):
    """View for managing jobs"""
    jobs = Job.objects.all().order_by('-created_at')
    companies = Company.objects.all().order_by('name')
    recruiters = Recruiter.objects.all()
    
    # Pagination
    paginator = Paginator(jobs, 10)  # Show 10 jobs per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'jobs': page_obj,
        'companies': companies,
        'recruiters': recruiters,
        'total_jobs': jobs.count(),
        'active_jobs': jobs.filter(is_active=True).count(),
    }
    return render(request, "administrator/jobs.html", context)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def job_create(request):
    """AJAX view to create a new job"""
    try:
        data = json.loads(request.body)
        
        company = Company.objects.get(id=data.get('company_id'))
        recruiter = Recruiter.objects.get(id=data.get('recruiter_id'))
        
        job = Job.objects.create(
            company=company,
            recruiter=recruiter,
            title=data.get('title'),
            job_type=data.get('job_type'),
            job_mode=data.get('job_mode'),
            salary_range=data.get('salary_range'),
            description=data.get('description'),
            responsibilities=data.get('responsibilities'),
            required_skills=data.get('required_skills'),
            interview_mode=data.get('interview_mode'),
            interview_date=timezone.datetime.strptime(data.get('interview_date'), '%Y-%m-%dT%H:%M'),
            number_of_openings=data.get('number_of_openings'),
            deadline=timezone.datetime.strptime(data.get('deadline'), '%Y-%m-%dT%H:%M'),
            is_active=data.get('is_active', True),
        )
        
        return JsonResponse({
            'status': 'success',
            'job_id': job.id,
            'message': 'Job created successfully!'
        })
    except Company.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Company not found'
        }, status=404)
    except Recruiter.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Recruiter not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["GET"])
def job_details(request, job_id):
    """AJAX view to get job details"""
    try:
        job = Job.objects.get(id=job_id)
        data = {
            'id': job.id,
            'company_id': job.company.id,
            'company_name': job.company.name,
            'recruiter_id': job.recruiter.id,
            'recruiter_name': job.recruiter.username,
            'title': job.title,
            'job_type': job.job_type,
            'job_mode': job.job_mode,
            'salary_range': job.salary_range,
            'description': job.description,
            'responsibilities': job.responsibilities,
            'required_skills': job.required_skills,
            'interview_mode': job.interview_mode,
            'interview_date': job.interview_date.strftime('%Y-%m-%dT%H:%M'),
            'number_of_openings': job.number_of_openings,
            'deadline': job.deadline.strftime('%Y-%m-%dT%H:%M'),
            'created_at': job.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': job.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': job.is_active,
            'applicant_count': job.applicants.count(),
        }
        return JsonResponse({
            'status': 'success',
            'job': data
        })
    except Job.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Job not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def job_update(request, job_id):
    """AJAX view to update job details"""
    try:
        job = Job.objects.get(id=job_id)
        data = json.loads(request.body)
        
        if 'company_id' in data:
            job.company = Company.objects.get(id=data.get('company_id'))
        
        if 'recruiter_id' in data:
            job.recruiter = Recruiter.objects.get(id=data.get('recruiter_id'))
        
        job.title = data.get('title', job.title)
        job.job_type = data.get('job_type', job.job_type)
        job.job_mode = data.get('job_mode', job.job_mode)
        job.salary_range = data.get('salary_range', job.salary_range)
        job.description = data.get('description', job.description)
        job.responsibilities = data.get('responsibilities', job.responsibilities)
        job.required_skills = data.get('required_skills', job.required_skills)
        job.interview_mode = data.get('interview_mode', job.interview_mode)
        
        if 'interview_date' in data:
            job.interview_date = timezone.datetime.strptime(data.get('interview_date'), '%Y-%m-%dT%H:%M')
        
        job.number_of_openings = data.get('number_of_openings', job.number_of_openings)
        
        if 'deadline' in data:
            job.deadline = timezone.datetime.strptime(data.get('deadline'), '%Y-%m-%dT%H:%M')
        
        job.is_active = data.get('is_active', job.is_active)
        job.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Job updated successfully!'
        })
    except Job.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Job not found'
        }, status=404)
    except Company.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Company not found'
        }, status=404)
    except Recruiter.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Recruiter not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def job_delete(request, job_id):
    """AJAX view to delete job"""
    try:
        job = Job.objects.get(id=job_id)
        job_title = job.title
        job.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Job "{job_title}" deleted successfully!'
        })
    except Job.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Job not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
def manage_company_uploads(request):
    """View for managing company uploads"""
    uploads = CompanyUpload.objects.all().order_by('-uploaded_at')
    companies = Company.objects.filter(is_active=True).order_by('name')
    
    # Pagination
    paginator = Paginator(uploads, 10)  # Show 10 uploads per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'uploads': page_obj,
        'companies': companies,
        'total_uploads': uploads.count(),
        'public_uploads': uploads.filter(is_public=True).count(),
    }
    return render(request, "administrator/company_uploads.html", context)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def company_upload_create(request):
    """AJAX view to create a new company upload"""
    try:
        # Handle file upload
        if 'file' in request.FILES:
            upload_file = request.FILES['file']
            company_id = request.POST.get('company_id')
            title = request.POST.get('title')
            description = request.POST.get('description')
            upload_type = request.POST.get('upload_type')
            external_url = request.POST.get('external_url', '')
            is_public = request.POST.get('is_public', 'true') == 'true'
            
            company = Company.objects.get(id=company_id)
            
            upload = CompanyUpload.objects.create(
                company=company,
                title=title,
                description=description,
                upload_type=upload_type,
                file=upload_file,
                external_url=external_url,
                is_public=is_public
            )
            
            # Add targeted students if not public
            if not is_public and 'target_students' in request.POST:
                student_ids = request.POST.getlist('target_students')
                for student_id in student_ids:
                    student = Student.objects.get(id=student_id)
                    upload.target_students.add(student)
            
            return JsonResponse({
                'status': 'success',
                'upload_id': upload.id,
                'message': 'Upload created successfully!'
            })
        else:
            # Handle form submission without file (external URL only)
            data = json.loads(request.body)
            
            company = Company.objects.get(id=data.get('company_id'))
            
            upload = CompanyUpload.objects.create(
                company=company,
                title=data.get('title'),
                description=data.get('description'),
                upload_type=data.get('upload_type'),
                external_url=data.get('external_url'),
                is_public=data.get('is_public', True)
            )
            
            # Add targeted students if not public
            if not data.get('is_public', True) and 'target_students' in data:
                for student_id in data.get('target_students', []):
                    student = Student.objects.get(id=student_id)
                    upload.target_students.add(student)
            
            return JsonResponse({
                'status': 'success',
                'upload_id': upload.id,
                'message': 'Upload created successfully!'
            })
            
    except Company.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Company not found'
        }, status=404)
    except Student.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'One or more selected students not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["GET"])
def company_upload_details(request, upload_id):
    """AJAX view to get company upload details"""
    try:
        upload = CompanyUpload.objects.get(id=upload_id)
        target_students = list(upload.target_students.values('id', 'username', 'email'))
        
        data = {
            'id': upload.id,
            'company_id': upload.company.id,
            'company_name': upload.company.name,
            'title': upload.title,
            'description': upload.description,
            'upload_type': upload.upload_type,
            'upload_type_display': upload.get_upload_type_display(),
            'file_url': upload.file.url if upload.file else None,
            'external_url': upload.external_url,
            'is_public': upload.is_public,
            'target_students': target_students,
            'uploaded_at': upload.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': upload.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return JsonResponse({
            'status': 'success',
            'upload': data
        })
    except CompanyUpload.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Upload not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def company_upload_update(request, upload_id):
    """AJAX view to update company upload details"""
    try:
        upload = CompanyUpload.objects.get(id=upload_id)
        
        # Handle file upload
        if 'file' in request.FILES:
            upload_file = request.FILES['file']
            company_id = request.POST.get('company_id', upload.company.id)
            title = request.POST.get('title', upload.title)
            description = request.POST.get('description', upload.description)
            upload_type = request.POST.get('upload_type', upload.upload_type)
            external_url = request.POST.get('external_url', upload.external_url)
            is_public = request.POST.get('is_public', 'true' if upload.is_public else 'false') == 'true'
            
            if int(company_id) != upload.company.id:
                upload.company = Company.objects.get(id=company_id)
            
            upload.title = title
            upload.description = description
            upload.upload_type = upload_type
            upload.file = upload_file
            upload.external_url = external_url
            upload.is_public = is_public
            upload.save()
            
            # Update targeted students
            upload.target_students.clear()
            if not is_public and 'target_students' in request.POST:
                student_ids = request.POST.getlist('target_students')
                for student_id in student_ids:
                    student = Student.objects.get(id=student_id)
                    upload.target_students.add(student)
        else:
            # Handle form submission without file update
            data = json.loads(request.body)
            
            if 'company_id' in data and data.get('company_id') != upload.company.id:
                upload.company = Company.objects.get(id=data.get('company_id'))
            
            upload.title = data.get('title', upload.title)
            upload.description = data.get('description', upload.description)
            upload.upload_type = data.get('upload_type', upload.upload_type)
            upload.external_url = data.get('external_url', upload.external_url)
            upload.is_public = data.get('is_public', upload.is_public)
            upload.save()
            
            # Update targeted students
            if 'target_students' in data:
                upload.target_students.clear()
                if not data.get('is_public', True):
                    for student_id in data.get('target_students', []):
                        student = Student.objects.get(id=student_id)
                        upload.target_students.add(student)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Upload updated successfully!'
        })
    except CompanyUpload.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Upload not found'
        }, status=404)
    except Company.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Company not found'
        }, status=404)
    except Student.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'One or more selected students not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def company_upload_delete(request, upload_id):
    """AJAX view to delete company upload"""
    try:
        upload = CompanyUpload.objects.get(id=upload_id)
        upload_title = upload.title
        
        # Delete file from storage if exists
        if upload.file:
            if os.path.isfile(upload.file.path):
                os.remove(upload.file.path)
        
        upload.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Upload "{upload_title}" deleted successfully!'
        })
    except CompanyUpload.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Upload not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)