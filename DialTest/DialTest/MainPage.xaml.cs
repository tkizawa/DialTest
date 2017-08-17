using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
using Windows.Foundation;
using Windows.Foundation.Collections;
using Windows.Storage.Streams;
using Windows.UI.Input;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Controls.Primitives;
using Windows.UI.Xaml.Data;
using Windows.UI.Xaml.Input;
using Windows.UI.Xaml.Media;
using Windows.UI.Xaml.Navigation;

// 空白ページの項目テンプレートについては、https://go.microsoft.com/fwlink/?LinkId=402352&clcid=0x411 を参照してください

namespace DialTest
{
    /// <summary>
    /// それ自体で使用できる空白ページまたはフレーム内に移動できる空白ページ。
    /// </summary>
    public sealed partial class MainPage : Page
    {
        RadialController myController;

        public MainPage()
        {
            this.InitializeComponent();
            // RadialControllerのインスタンスを作成する
            myController = RadialController.CreateForCurrentView();

            // カスタムツールのアイコンを作成する
            RandomAccessStreamReference icon = RandomAccessStreamReference.CreateFromUri(new Uri("ms-appx:///Assets/StoreLogo.png"));

            // メニューの作成
            RadialControllerMenuItem myItem =
                RadialControllerMenuItem.CreateFromIcon("ぐるぐるSurface Dial", icon);

            // メニューの追加
            myController.Menu.Items.Add(myItem);

            // ハンドラの追加
            myController.ButtonClicked += MyController_ButtonClicked;
            myController.RotationChanged += MyController_RotationChanged;
        }

        // ハンドラ
        private void MyController_RotationChanged(RadialController sender,RadialControllerRotationChangedEventArgs args)
        {
            if(RotationSlider.Value+args.RotationDeltaInDegrees > 100)
            {
                RotationSlider.Value = 100;
                return;
            }
            else if(RotationSlider.Value+args.RotationDeltaInDegrees<0)
            {
                RotationSlider.Value = 0;
                return;
            }
            RotationSlider.Value += args.RotationDeltaInDegrees;
        }

        private void MyController_ButtonClicked(RadialController sender,RadialControllerButtonClickedEventArgs args)
        {
            ButtonToggle.IsOn = !ButtonToggle.IsOn;
        }
    }
}
