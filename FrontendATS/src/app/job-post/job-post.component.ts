import { Component, OnInit } from '@angular/core';
import { JobPostService } from '../services/job-post.service';

@Component({
  selector: 'app-job-post',
  templateUrl: './job-post.component.html',
  styleUrls: ['./job-post.component.css']
})
export class JobPostComponent implements OnInit {
  public posts;
  constructor(private JobPostService:JobPostService) { }

  ngOnInit(): void {
    this.getPosts();
  }

  dataURItoBlob(dataURI) {
    const byteString = window.atob(dataURI);
    const arrayBuffer = new ArrayBuffer(byteString.length);
    const int8Array = new Uint8Array(arrayBuffer);
    for (let i = 0; i < byteString.length; i++) {
      int8Array[i] = byteString.charCodeAt(i);
    }
    const blob = new Blob([int8Array], { type: 'image/png' });
    return blob;
 }

  getPosts() {
    this.JobPostService.list().subscribe(
      // the first argument is a function which runs on success
      data => {
        this.posts = data;
        for (let post of this.posts) {
          post.date_updated = new Date(post.date_updated);
          let url = "http://127.0.0.1:8000/";
          let filepath = post.image;
          post.image = url + filepath.substr(1);

        }

      },
      err => console.error(err),
      () => console.log('done loading posts')

    );


  }

  save_title(title){
    localStorage.setItem('title',JSON.stringify(title));
  }

}
