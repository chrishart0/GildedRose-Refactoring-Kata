#!/bin/python3
# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose

class GildedRoseTest(unittest.TestCase):

    def item_are_valid_tests(self, items):
        '''
        A series of constraints an item should always abide by
        Use this on every test
        '''
        valid = True
        for item in items:
            #Verify item quality is not negative
            if ( item.quality < 0 ):
                valid = False
            
            #Verify item quality is greater than 50
            if ( item.quality > 50 ):
                valid = False
        
        return valid

    def test_EOD_SellIn_value_lowered_1(self):
        #Define test item 
        items = [
            Item(name="+5 Dexterity Vest", sell_in=10, quality=20),
        ]
        #Save sell_in value for use in the assert
        day0_sell_in = items[0].sell_in

        #Iterate one day
        GildedRose(items).update_quality()
        
        #Verify sell_in has changed by -1
        day1_sell_in = items[0].sell_in
        self.assertTrue(day0_sell_in == (day1_sell_in + 1))
        self.assertTrue(self.item_are_valid_tests(items))

    #TODO: also test what happens when value is at 1 then iterated
    def test_EOD_Quality_value_lowered(self): 
        #Define test item
        items = [
            Item(name="+5 Dexterity Vest", sell_in=10, quality=2),
        ]
        #save quality value for use in the assert
        day0_quality = items[0].quality

        #Iterate one day
        GildedRose(items).update_quality()

        #Verify quality has been reduced by any amount
        day1_quality = items[0].quality
        self.assertGreater(day0_quality, day1_quality)
        self.assertTrue(self.item_are_valid_tests(items))

    def test_item_past_expiration_quality_degrades_double(self):
        #Define test item
        items = [
            Item(name="+5 Dexterity Vest", sell_in=1, quality=20),
        ]
        #Save quality value for use in the assert
        day0_quality = items[0].quality

        #Iterate 2 days, saving quality data for testing
        GildedRose(items).update_quality() #Iterate one day
        day1_quality = items[0].quality
        GildedRose(items).update_quality() #Iterate one day
        day2_quality = items[0].quality

        #Calculated differences between days
        diff_day0_day1 = day0_quality - day1_quality
        diff_day1_day2 = day1_quality - day2_quality
        #Verify when item has "Expired" it loses value twice as fast
        #Diff between day1 and day2 should be double diff between day0 and day1 because sell_in is then less than 1
        self.assertEqual(diff_day1_day2, (diff_day0_day1*2))
        self.assertTrue(self.item_are_valid_tests(items))

    def test_quality_does_not_decrease_under_0(self):
        #Define test item
        items = [
            Item(name="+5 Dexterity Vest", sell_in=10, quality=0),
        ]

        #Iterate one day
        GildedRose(items).update_quality()

        #Verify quality has been reduced by any amount
        final_quality = items[0].quality
        self.assertGreaterEqual(final_quality, 0)
        self.assertTrue(self.item_are_valid_tests(items))

    def test_quality_never_over_50(self):
        '''
        We are assuming that item quality never input as over 50
        Most items go down in quality, we are using Backstage passes amd Brie because they go up
        Aged Brie will go:        49 > 50 > 51
        Backstage Passes will go: 49 > 52 > 55
        '''
        params = [
            Item(name="Aged Brie", sell_in=10, quality=49),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=3, quality=49),
        ]

        for param in params:
            with self.subTest(param=param):
                items = [
                    param,
                ]

                #Iterate one day
                GildedRose(items).update_quality()
                GildedRose(items).update_quality()

                #Verify quality has raised by any amount
                final_quality = items[0].quality

                
                self.assertTrue(self.item_are_valid_tests(items))

    def test_exception_items_increase_quality_over_time(self):
        '''
        'Aged Brie' and 'Backstage passes to a TAFKAL80ETC concert' are exception to the rule that quality goes down over time
        'Aged Brie' and 'Backstage passes to a TAFKAL80ETC concert' quality value goes up over time
        '''
        params = [
            Item(name="Aged Brie", sell_in=10, quality=20),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=20),
        ]

        for param in params:
            with self.subTest(param=param):
                items = [
                    param,
                ]
                #save quality value for use in the assert
                day0_quality = items[0].quality

                #Iterate one day
                GildedRose(items).update_quality()

                #Verify quality has raised by any amount
                day1_quality = items[0].quality

                self.assertGreater(day1_quality, day0_quality)
                self.assertTrue(self.item_are_valid_tests(items))

    def test_backstage_pass_increase_by_2_days_10_to_6(self):

        for i in range(6, 11):
            with self.subTest(i=i):
                items = [
                    Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=i, quality=20),
                ]
                #save quality value for use in the assert
                day0_quality = items[0].quality

                #Iterate one day
                GildedRose(items).update_quality()

                #Verify quality has raised by any amount
                day1_quality = items[0].quality

                self.assertEqual(day1_quality, (day0_quality + 2))
                self.assertTrue(self.item_are_valid_tests(items))

    def test_backstage_pass_increase_by_3_days_5_to_0(self):

        for i in range(1, 6):
            with self.subTest(i=i):
                items = [
                    Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=i, quality=20),
                ]
                #save quality value for use in the assert
                day0_quality = items[0].quality

                #Iterate one day
                GildedRose(items).update_quality()

                #Verify quality has raised by any amount
                day1_quality = items[0].quality

                self.assertEqual(day1_quality, (day0_quality + 3))
                self.assertTrue(self.item_are_valid_tests(items))
        
    def test_backstage_pass_quality_0_past_sell_in_date(self):
        items = [
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=20),
        ]

        #Iterate one day
        GildedRose(items).update_quality()
        #Verify quality has raised by any amount
        final_quality = items[0].quality

        self.assertEqual(final_quality, 0)
        
if __name__ == '__main__':
    unittest.main()
