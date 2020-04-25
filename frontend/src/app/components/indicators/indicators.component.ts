import { Component, OnInit, OnChanges, Input } from '@angular/core';
import { DataService } from '../../services/data.service';
import { MatProgressSpinner } from '@angular/material'



@Component({
  selector: 'app-indicators',
  templateUrl: './indicators.component.html',
  styleUrls: ['./indicators.component.css'],
})
export class IndicatorsComponent implements OnInit {
  constructor(private dataService:DataService) { }

  @Input() modelID:string;

  data:any[];
  loading:boolean;

  ngOnInit() {
    console.log('model ID is', this.modelID);
  }

  ngOnChanges() {
    // create header using child_id
    console.log('model is', this.modelID);
    this.loading = true;

    this.dataService.getModelInformation(this.modelID).subscribe(result => {
      this.loading = false;
      this.data = result['data'];
    })
  }
  

}
