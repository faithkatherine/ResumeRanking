import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, FormBuilder, Validators} from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-add-resumes',
  templateUrl: './add-resumes.component.html',
  styleUrls: ['./add-resumes.component.css']
})
export class AddResumesComponent implements OnInit {

  auth_url:string = 'http://localhost:8000/api/resumes';

  form: FormGroup;
  jsonHeader = {headers: new HttpHeaders()};
  constructor(private fb: FormBuilder, private httpClient: HttpClient, private router: Router) {
    this.form = this.fb.group({
      Applicant_name : [''],
      jobpost_title : [''],
      document: [null]
    });
  }

  uploadFile(event) {
    const file = (event.target as HTMLInputElement).files[0];
    this.form.patchValue({
      document: file
    });
    this.form.get('document').updateValueAndValidity()
  }

  addResumePost(){
    const formData = new FormData();
    formData.append( 'Applicant_name', this.form.get('Applicant_name').value);
    formData.append( 'document', this.form.get('document').value);
    formData.append('jobpost_title', JSON.parse(localStorage.getItem('title'))),
    this.httpClient.post(
      this.auth_url + '/create/',
      formData,
      /*jobpost_title,*/
      this.jsonHeader
    ).subscribe(
      (response:any) => {
        console.log(response);

      })
      this.router.navigate(['/jobpost']);

  }

  ngOnInit(): void {
  }

}
