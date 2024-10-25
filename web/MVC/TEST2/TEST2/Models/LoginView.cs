using System.ComponentModel.DataAnnotations;

namespace TEST2.Models
{
    public class LoginView
    {
        [Required]
        public string Username { get; set; }

        [Required]
        [DataType(DataType.Password)]
        public string Password { get; set; }
    }
}
