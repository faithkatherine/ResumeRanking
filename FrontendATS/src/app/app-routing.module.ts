import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AccountComponent } from './account/account.component';
import { HomeComponent } from './home/home.component';
import { JobPostComponent } from './job-post/job-post.component';
import { ResumePostComponent } from './resume-post/resume-post.component';
import { LoginComponent } from './login/login.component';
import { RegistrationComponent } from './registration/registration.component';
import {AuthGuard } from './auth.guard';
import { AddJobPostComponent } from './add-job-post/add-job-post.component';
import { AddResumesComponent } from './add-resumes/add-resumes.component';
import {ResumeBuilderComponent} from './resume-builder/resume-builder.component';


const routes: Routes = [
  {path:'home', component:HomeComponent},
  {path:'account', component:AccountComponent},
  {path:'jobpost', component:JobPostComponent},
  {path:'resumepost', component:ResumePostComponent},
  {path: 'login', component: LoginComponent},
  {path: 'registration', component: RegistrationComponent},
  {path: 'account', component: AccountComponent, canActivate: [AuthGuard]},
  {path: 'createjob', component: AddJobPostComponent},
  {path: 'create-resume', component:AddResumesComponent},
  {path: 'build-resume', component:ResumeBuilderComponent},
  {path:'' , redirectTo:'home', pathMatch: 'full'}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
