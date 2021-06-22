import { TestBed } from '@angular/core/testing';

import { AddjobpostService } from './addjobpost.service';

describe('AddjobpostService', () => {
  let service: AddjobpostService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AddjobpostService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
