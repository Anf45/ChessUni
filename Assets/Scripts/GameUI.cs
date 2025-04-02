using System;
using System.Threading;
using TMPro;
using UnityEngine;

public enum CameraAngle
{
    menu = 0, 
    whiteTeam = 1, 
    blackTeam = 2
}

public class GameUI : MonoBehaviour
{
    public static GameUI instance { set; get; }

    public Server server;
    public Client client;

    [SerializeField] private Animator menuAnimator;
    [SerializeField] private TMP_InputField addressInput;
    [SerializeField] private GameObject[] cameraAngles;

    public Action<bool> SetLocalGame;

    private void Awake()
    {
        instance = this;
        RegisterEvents();
    }

    //camera
    public void ChangeCamera(CameraAngle index)
    {
        for (int i = 0; i < cameraAngles.Length; i++)
            cameraAngles[i].SetActive(false);

        cameraAngles[(int)index].SetActive(true);

    }

    //buttons 
    public void OnLocalGameButton()
    {
        Debug.Log("Starting Local Game: Initializing Server...");
        SetLocalGame?.Invoke(true);
        menuAnimator.SetTrigger("InGameMenu");
        server.Init(8007);
        client.Init("127.0.0.1", 8007);

    }
    public void OnOnlineGameButton()
    {
        menuAnimator.SetTrigger("OnlineMenu");

    }

    public void OnOnlineHostButton()
    {
        SetLocalGame?.Invoke(false);

        server.Init(8007);
        client.Init("127.0.0.1", 8007);
        menuAnimator.SetTrigger("HostMenu");

    }
    public void OnOnlineConnectButton()
    {
        SetLocalGame?.Invoke(false);

        client.Init(addressInput.text, 8007);
        //Debug.Log("OnOnlineConnectButton"); //$$

    }

    public void OnOnlineBackButton()
    {
        menuAnimator.SetTrigger("StartMenu");

    }
    public void OnHostBackButton()
    {
        server.Shutdown();
        client.Shutdown();
        menuAnimator.SetTrigger("OnlineMenu");

    }

    public void OnLeaveFromGameMenu()
    {
        ChangeCamera(CameraAngle.menu);
        menuAnimator.SetTrigger("StartMenu");
    }

    #region
    private void RegisterEvents()
    {

        NetUtility.C_START_GAME += OnStartGameClient;
    }

    private void UnRegisterEvents()
    {
        NetUtility.C_START_GAME -= OnStartGameClient;

    }
    private void OnStartGameClient(NetMessage obj)
    {
        menuAnimator.SetTrigger("InGameMenu");
    }
    #endregion
}
