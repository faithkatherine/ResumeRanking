import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, FormBuilder, Validators } from '@angular/forms';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';


@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})
export class RegistrationComponent implements OnInit {
  form: FormGroup;
  constructor(private fb: FormBuilder, private authService: AuthService, private router: Router) {
    this.form = this.fb.group({
      email   : new FormControl('', Validators.compose([Validators.required, Validators.minLength(10)])),
      username: new FormControl('', Validators.compose([Validators.required, Validators.minLength(10)])),
      password: new FormControl('', Validators.compose([Validators.required, Validators.minLength(6)])),
      password2:new FormControl('', Validators.compose([Validators.required, Validators.minLength(6)]))
    });
  }

  signUpUser(){
    this.authService.signUp(
      this.form.get('email').value,
      this.form.get('username').value,
      this.form.get('password').value,
      this.form.get('password2').value
    ).subscribe(
      (response:any) => {
        console.log(response);
        if(response['status'] == 'successfully registered new user'){
        this.form.reset();
        this.router.navigate(['login']);
        }
      }
    )
  }

  ngOnInit(): void {
  }
}
