using UnityEngine;
using UnityEngine.InputSystem;

[RequireComponent(typeof(CharacterController))]
public class PlayerMovement : MonoBehaviour
{
    private PlayerControls controls;
    private CharacterController controller;

    private Vector2 moveInput;
    private Vector2 lookInput;

    [Header("Movement")]
    public float walkSpeed = 3f;
    public float runSpeed = 5.5f;
    public float crouchSpeed = 1.5f;
    private float currentSpeed;

    [Header("Jump")]
    public float jumpHeight = 1.2f;
    public float gravity = -9.81f;
    private float velocityY;

    [Header("Crouch")]
    public float crouchHeight = 1.1f;
    public float normalHeight = 1.8f;
    private bool isCrouching = false;

    [Header("Camera")]
    public float sensitivity = 0.05f;   // Чувствительность для новой Input System
    public Transform cameraHolder;
    private float cameraPitch = 0f;

    private void Awake()
    {
        controls = new PlayerControls();

        controls.Player.Move.performed += ctx => moveInput = ctx.ReadValue<Vector2>();
        controls.Player.Move.canceled += ctx => moveInput = Vector2.zero;

        controls.Player.Look.performed += ctx => lookInput = ctx.ReadValue<Vector2>();
        controls.Player.Look.canceled += ctx => lookInput = Vector2.zero;

        controls.Player.Jump.performed += Jump;
        controls.Player.Crouch.performed += Crouch;

        controls.Player.Run.performed += ctx => currentSpeed = runSpeed;
        controls.Player.Run.canceled += ctx => currentSpeed = walkSpeed;
    }

    private void Start()
    {
        controller = GetComponent<CharacterController>();
        currentSpeed = walkSpeed;

        // ВАЖНО! Без этого мышка не работает.
        Cursor.lockState = CursorLockMode.Locked;
        Cursor.visible = false;
    }

    private void Update()
    {
        Move();
        LookAround();
    }

    private void Move()
    {
        bool grounded = controller.isGrounded;

        if (grounded && velocityY < 0)
            velocityY = -2f;

        Vector3 move = transform.right * moveInput.x + transform.forward * moveInput.y;
        controller.Move(move * currentSpeed * Time.deltaTime);

        // gravity
        velocityY += gravity * Time.deltaTime;
        controller.Move(Vector3.up * velocityY * Time.deltaTime);
    }

    private void LookAround()
    {
        float mouseX = lookInput.x * sensitivity;
        float mouseY = lookInput.y * sensitivity;

        // Поворот тела игрока по горизонтали
        transform.Rotate(Vector3.up * mouseX);

        // Поворот камеры по вертикали
        cameraPitch -= mouseY;
        cameraPitch = Mathf.Clamp(cameraPitch, -80f, 80f);
        cameraHolder.localRotation = Quaternion.Euler(cameraPitch, 0f, 0f);
    }

    private void Jump(InputAction.CallbackContext ctx)
    {
        if (controller.isGrounded)
            velocityY = Mathf.Sqrt(jumpHeight * -2f * gravity);
    }

    private void Crouch(InputAction.CallbackContext ctx)
    {
        if (!isCrouching)
        {
            controller.height = crouchHeight;
            currentSpeed = crouchSpeed;
            isCrouching = true;
        }
        else
        {
            controller.height = normalHeight;
            currentSpeed = walkSpeed;
            isCrouching = false;
        }
    }

    private void OnEnable() => controls.Enable();
    private void OnDisable() => controls.Disable();
}
