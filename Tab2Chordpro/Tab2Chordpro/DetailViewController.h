//
//  DetailViewController.h
//  Tab2Chordpro
//
//  Created by Magnus Olsson on 3/31/13.
//  Copyright (c) 2013 Magnus Olsson. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface DetailViewController : UIViewController <UISplitViewControllerDelegate>

@property (strong, nonatomic) id detailItem;

@property (weak, nonatomic) IBOutlet UILabel *detailDescriptionLabel;
@end
