#include <vector>
#include <functional>
#include <stdio.h>


class command_reader
{
public:


    enum 
    {
    STATE_INIT = 0, 
    STATE_HEADER_FOUND = 1
    };


    command_reader(std::function <void (const unsigned char*,int)> callback_): 
    callback{callback_}, 
    header{0xfe},
    lenCMD{8}
    {
        // printf("header %02x \n",header[0]);
    }


    ~command_reader()
    {
    }


    void feedData(unsigned char * data, int len)
    {
        for (int i = 0; i < len; i++)
        {
            unsigned char & byteData = data[i];

            if (byteData == this->header[0])
            {
                this->buffer.clear();
            }
            
            this->buffer.push_back(byteData);

            if ( this->buffer.size() == this->lenCMD )
            {
                if ( this->checkSum(this->buffer.data(),this->lenCMD) )
                {
                    this->callback(this->buffer.data(),this->lenCMD);
                }
                this->buffer.clear();
            }            
        }
    }





private:


    bool checkSum(const unsigned char * data, int len)
    {    
        bool result = false;

        if (len > 1)
        {
            int i;
            unsigned char sum = 0;

            for (i = 0; i < len - 1; i++)
            {
                sum += data[i];
            }
            result = ( sum == data[len-1]?true:false );
        }
        
        return result;
    }


    std::function <void (const unsigned char*,int)> callback;
    int             state;
    const unsigned char header[1];
    const int       lenCMD;
    std::vector < unsigned char > buffer;
};

int main()
{
    auto callback=[=](const unsigned char *data,int len){
        printf("Command Arrived:");
        for (int i=0;i<len;i++){
                printf("%02x ",data[i]);
            }
        printf("\n");
        };
    command_reader reader(callback);
    unsigned char data[]={0xfe,0xfe,0,0,0,0,1,0x1f,0x1e,0xfe,1,0,0,0,0,0,0xff,0xfe};
    reader.feedData(data,sizeof(data));
    return 0;
}


