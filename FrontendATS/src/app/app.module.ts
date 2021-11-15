import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {HttpClientModule, HTTP_INTERCEPTORS} from '@angular/common/http';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { UserRequestInterceptor } from './interceptor';
import { RichTextEditorAllModule } from '@syncfusion/ej2-angular-richtexteditor';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AccountComponent } from './account/account.component';
import { ResumePostComponent } from './resume-post/resume-post.component';
import { JobPostComponent } from './job-post/job-post.component';
import { HomeComponent } from './home/home.component';
import { RegistrationComponent } from './registration/registration.component';
import { AuthComponent } from './auth/auth.component';
import { LoginComponent } from './login/login.component';
import { AddJobPostComponent } from './add-job-post/add-job-post.component';
import { AddResumesComponent } from './add-resumes/add-resumes.component';
import { ResumeBuilderComponent } from './resume-builder/resume-builder.component';

@NgModule({
  declarations: [
    AppComponent,
    AccountComponent,
    ResumePostComponent,
    JobPostComponent,
    HomeComponent,
    RegistrationComponent,
    AuthComponent,
    LoginComponent,
    AddJobPostComponent,
    AddResumesComponent,
    ResumeBuilderComponent
  ],
  entryComponents: [
    JobPostComponent
  ],

  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule,
    RichTextEditorAllModule,

  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: UserRequestInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
