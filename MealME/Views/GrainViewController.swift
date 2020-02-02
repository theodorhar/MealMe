//
//  GrainViewController.swift
//  MealME
//
//  Created by Tanay Kane on 2/1/20.
//  Copyright © 2020 Theodor Har. All rights reserved.
//

import UIKit

class GrainViewController: UIViewController {
let repo = Repository()
    
    @IBAction func breadPressed(_ sender: Any) {
        API.ingredients.insert("bread")
    }
    
    @IBAction func ricePressed(_ sender: Any) {
        API.ingredients.insert("rice")
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
